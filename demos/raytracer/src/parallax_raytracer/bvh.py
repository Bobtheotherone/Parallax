"""Deterministic binned surface-area-heuristic BVH. Leaves contain at most four finite primitives."""
from __future__ import annotations

from dataclasses import dataclass
import math

from .geometry import Bounds, Hit, Primitive, Ray


@dataclass(slots=True)
class TraversalStats:
    box_tests: int = 0
    primitive_tests: int = 0


@dataclass(frozen=True, slots=True)
class Node:
    bounds: Bounds
    left: int = -1
    right: int = -1
    indices: tuple[int, ...] = ()


class BVH:
    """Read-only after construction; traversal state belongs to each invocation."""

    def __init__(self, objects: tuple[Primitive, ...]):
        self.objects = objects
        nodes: list[Node] = []

        def build(indices: list[int]) -> int:
            bounds = objects[indices[0]].bounds
            for index in indices[1:]:
                bounds = bounds.union(objects[index].bounds)
            slot = len(nodes)
            nodes.append(Node(bounds))
            if len(indices) <= 2:
                nodes[slot] = Node(bounds, indices=tuple(sorted(indices)))
                return slot
            # Compare expected primitive work on the two child surface areas.
            # Binning limits build cost; tie order is axis then bin then scene ID.
            best_cost, best_partition = math.inf, None
            spans = []
            for axis in range(3):
                low = min(objects[i].bounds.centroid(axis) for i in indices)
                span = max(objects[i].bounds.centroid(axis) for i in indices) - low
                spans.append(span)
                if span == 0.0:
                    continue
                bins: list[list[int]] = [[] for _ in range(12)]
                for index in indices:
                    bucket = min(11, int(12 * ((objects[index].bounds.centroid(axis) - low) / span)))
                    bins[bucket].append(index)
                # Prefix/suffix scans avoid quadratic primitive work during build.
                prefix, suffix = [], []
                for ordered, destination in ((bins, prefix), (list(reversed(bins)), suffix)):
                    count, extent = 0, None
                    for bucket in ordered:
                        for index in bucket:
                            extent = objects[index].bounds if extent is None else extent.union(objects[index].bounds)
                        count += len(bucket)
                        destination.append((count, extent))
                for split in range(11):
                    ln, lb = prefix[split]
                    rn, rb = suffix[10-split]
                    if not ln or not rn:
                        continue
                    cost = ln * lb.area() + rn * rb.area()
                    if cost < best_cost:
                        best_cost = cost
                        best_partition = ([i for bucket in bins[:split+1] for i in bucket],
                                          [i for bucket in bins[split+1:] for i in bucket])
            if len(indices) <= 4 and (best_partition is None or best_cost + bounds.area() >= len(indices) * bounds.area()):
                nodes[slot] = Node(bounds, indices=tuple(sorted(indices)))
                return slot
            if best_partition is None:
                axis = max(range(3), key=spans.__getitem__)
                indices.sort(key=lambda i: (objects[i].bounds.centroid(axis), i))
                midpoint = len(indices) // 2
                best_partition = indices[:midpoint], indices[midpoint:]
            left, right = build(best_partition[0]), build(best_partition[1])
            nodes[slot] = Node(bounds, left, right)
            return slot

        if objects:
            build(list(range(len(objects))))
        self.nodes = tuple(nodes)

    def nearest(self, ray: Ray, t_min: float = 0.0, t_max: float = math.inf,
                stats: TraversalStats | None = None) -> Hit | None:
        if not self.nodes or t_max <= t_min:
            return None
        if stats is not None:
            stats.box_tests += 1
        entry = self.nodes[0].bounds.entry(ray, t_min, t_max)
        if entry is None:
            return None
        stack = [(0, entry)]
        closest, winner = t_max, -1
        while stack:
            index, near = stack.pop()
            if near > closest:
                continue
            node = self.nodes[index]
            if node.indices:
                for obj_index in node.indices:
                    if stats is not None:
                        stats.primitive_tests += 1
                    t = self.objects[obj_index].intersect(ray, t_min, closest)
                    if t is not None and (winner < 0 or t < closest or
                                          (t == closest and obj_index < winner)):
                        closest, winner = t, obj_index
            else:
                if stats is not None:
                    stats.box_tests += 2
                left = self.nodes[node.left].bounds.entry(ray, t_min, closest)
                right = self.nodes[node.right].bounds.entry(ray, t_min, closest)
                # Far child pushed first. Once a near hit is found, stale far
                # entries are pruned against the updated closest distance.
                if left is not None and right is not None:
                    if left <= right:
                        stack.append((node.right, right))
                        stack.append((node.left, left))
                    else:
                        stack.append((node.left, left))
                        stack.append((node.right, right))
                elif left is not None:
                    stack.append((node.left, left))
                elif right is not None:
                    stack.append((node.right, right))
        return Hit.make(ray, closest, self.objects[winner], winner) if winner >= 0 else None


def brute_force(objects: tuple[Primitive, ...], ray: Ray, t_min: float = 0.0,
                t_max: float = math.inf, stats: TraversalStats | None = None) -> Hit | None:
    """Simple independent traversal for differential checks, not normal rendering."""
    best, winner = t_max, -1
    for index, primitive in enumerate(objects):
        if stats is not None:
            stats.primitive_tests += 1
        t = primitive.intersect(ray, t_min, best)
        if t is not None and (winner < 0 or t < best):
            best, winner = t, index
    return Hit.make(ray, best, objects[winner], winner) if winner >= 0 else None
