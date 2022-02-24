from __future__ import annotations
import math
from javascript import require

Vec3 = require("vec3")


class Vector3:
    def __init__(self, *inp) -> None:

        if len(inp) == 3:
            self.x = inp[0]
            self.y = inp[1]
            self.z = inp[2]

        elif len(inp) == 1:
            if isinstance(inp[0], tuple) or isinstance(inp[0], list):
                self.x = inp[0][0]
                self.y = inp[0][1]
                self.z = inp[0][2]
            else:
                self.x = inp[0].x
                self.y = inp[0].y
                self.z = inp[0].z
        else:
            raise Exception()

    def distanceTo(self, target) -> float:
        dx = target.x - self.x
        dy = target.y - self.y
        dz = target.z - self.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def distanceSquaredTo(self, target) -> float:
        dx = target.x - self.x
        dy = target.y - self.y
        dz = target.z - self.z
        return dx * dx + dy * dy + dz * dz

    def xzDistanceTo(self, target) -> float:
        dx = target.x - self.x
        dz = target.z - self.z
        return math.sqrt(dx * dx + dz * dz)

    def add(self, target) -> Vector3:
        return Vector3(self.x + target.x, self.y + target.y, self.z + target.z)

    def subtract(self, target) -> Vector3:
        return Vector3(target.x - self.x, target.y - self.y, target.z - self.z)

    def multiply(self, target) -> Vector3:
        return Vector3(target.x * self.x, target.y * self.y, target.z * self.z)

    def abs(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self) -> Vector3:
        absolute = self.abs()
        if absolute == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / absolute, self.y / absolute, self.z / absolute)

    def toVec3(self) -> Vec3:
        return Vec3(self.x, self.y, self.z)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Vector3):
            return self.x == __o.x and self.y == __o.y and self.z == __o.z
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __str__(self) -> str:
        return f"(x:{self.x},y:{self.y},z:{self.z})"
