#!/usr/bin/env python3
"""Build editable Blender source and GLB exports for AI Investment Arena.

Run from the Godot project root:
  blender --background --factory-startup --python blender/build_ai_arena_assets.py -- --output assets
"""
import argparse
import json
import math
import os
import sys

import bpy
from mathutils import Vector

PROJECT_ROOT = os.getcwd()
DEFAULT_OUTPUT = "assets"
FACTIONS = [
    {"id": "value", "spriteX": 0, "spriteY": 0, "roomX": 0, "roomY": 0, "accent": (0.91, 0.70, 0.39, 1), "hair": (0.52, 0.51, 0.48, 1), "skin": (0.72, 0.53, 0.40, 1), "suit": (0.10, 0.12, 0.14, 1), "shirt": (0.83, 0.81, 0.74, 1), "style": "library"},
    {"id": "growth", "spriteX": 1, "spriteY": 0, "roomX": 1, "roomY": 0, "accent": (0.26, 0.77, 0.53, 1), "hair": (0.12, 0.08, 0.07, 1), "skin": (0.86, 0.66, 0.53, 1), "suit": (0.78, 0.75, 0.67, 1), "shirt": (0.16, 0.37, 0.28, 1), "style": "glass"},
    {"id": "trend", "spriteX": 2, "spriteY": 0, "roomX": 2, "roomY": 0, "accent": (0.36, 0.60, 0.86, 1), "hair": (0.06, 0.07, 0.08, 1), "skin": (0.66, 0.46, 0.35, 1), "suit": (0.06, 0.10, 0.15, 1), "shirt": (0.10, 0.19, 0.29, 1), "style": "trading"},
    {"id": "quant", "spriteX": 0, "spriteY": 1, "roomX": 0, "roomY": 1, "accent": (0.69, 0.50, 0.88, 1), "hair": (0.10, 0.08, 0.12, 1), "skin": (0.84, 0.64, 0.53, 1), "suit": (0.14, 0.14, 0.19, 1), "shirt": (0.27, 0.20, 0.38, 1), "style": "compute"},
    {"id": "sentiment", "spriteX": 1, "spriteY": 1, "roomX": 1, "roomY": 1, "accent": (0.91, 0.53, 0.31, 1), "hair": (0.08, 0.05, 0.04, 1), "skin": (0.88, 0.66, 0.53, 1), "suit": (0.12, 0.11, 0.12, 1), "shirt": (0.25, 0.14, 0.11, 1), "style": "media"},
    {"id": "macro", "spriteX": 2, "spriteY": 1, "roomX": 2, "roomY": 1, "accent": (0.40, 0.79, 0.82, 1), "hair": (0.61, 0.62, 0.63, 1), "skin": (0.78, 0.57, 0.45, 1), "suit": (0.18, 0.25, 0.31, 1), "shirt": (0.11, 0.22, 0.28, 1), "style": "global"},
]

MATERIALS = {}

def material(name, color, metallic=0.0, roughness=0.48):
    key = (name, tuple(color), metallic, roughness)
    if key in MATERIALS:
        return MATERIALS[key]
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    MATERIALS[key] = mat
    return mat

def image_material(name, image_path):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Roughness"].default_value = 1.0
    if os.path.exists(image_path):
        image = bpy.data.images.load(image_path, check_existing=True)
        image.pack()
        tex = nodes.new("ShaderNodeTexImage")
        tex.image = image
        tex.interpolation = "Linear"
        links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (0.07, 0.10, 0.13, 1)
    return mat

def collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col

def move_to(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def assign(obj, mat):
    if mat:
        obj.data.materials.append(mat)
    return obj

def bevel(obj, width=0.04, segments=3):
    if width <= 0:
        return obj
    mod = obj.modifiers.new("Soft machined edges", "BEVEL")
    mod.width = width
    mod.segments = segments
    obj.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    return obj

def cube(name, loc, scale, mat, col, bevel_width=0.035):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = move_to(bpy.context.object, col)
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(obj, mat)
    bevel(obj, bevel_width)
    return obj

def sphere(name, loc, scale, mat, col, segments=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=1, location=loc)
    obj = move_to(bpy.context.object, col)
    obj.name = name
    obj.scale = scale
    assign(obj, mat)
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj

def cylinder(name, loc, radius, depth, mat, col, vertices=32, rotation=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    obj = move_to(bpy.context.object, col)
    obj.name = name
    if rotation is not None:
        obj.rotation_euler = rotation
    assign(obj, mat)
    bevel(obj, min(radius * 0.12, 0.035), 2)
    return obj

def torus(name, loc, major, minor, mat, col, rotation=None):
    bpy.ops.mesh.primitive_torus_add(major_segments=32, minor_segments=8, location=loc, major_radius=major, minor_radius=minor)
    obj = move_to(bpy.context.object, col)
    obj.name = name
    if rotation is not None:
        obj.rotation_euler = rotation
    assign(obj, mat)
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj

def rod(name, start, end, radius, mat, col, vertices=16):
    a = Vector(start)
    b = Vector(end)
    direction = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=direction.length, location=(a + b) / 2)
    obj = move_to(bpy.context.object, col)
    obj.name = name
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = direction.to_track_quat("Z", "Y")
    assign(obj, mat)
    bevel(obj, radius * 0.2, 2)
    return obj

def plane(name, loc, width, height, mat, col, rotation=(math.pi / 2, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    obj = move_to(bpy.context.object, col)
    obj.name = name
    obj.scale = (width, height, 1)
    obj.rotation_euler = rotation
    assign(obj, mat)
    return obj

def apply_atlas_uv(obj, column, row):
    uv_layer = obj.data.uv_layers.active
    if uv_layer is None:
        return
    u0, u1 = column / 3.0, (column + 1) / 3.0
    if row == 0:
        v0, v1 = 0.5, 1.0
    else:
        v0, v1 = 0.0, 0.5
    for loop in uv_layer.data:
        loop.uv.x = u0 + loop.uv.x * (u1 - u0)
        loop.uv.y = v0 + loop.uv.y * (v1 - v0)

def add_monitor(col, x, y, z, accent, width=1.35, height=0.82, tilt=0.0):
    frame = material("Monitor frame", (0.018, 0.026, 0.034, 1), 0.45, 0.28)
    screen = material("Screen glow " + str(accent), (0.035, 0.075, 0.09, 1), 0.15, 0.25)
    cube("Monitor bezel", (x, y, z), (width, 0.10, height), frame, col, 0.055)
    cube("Abstract market display", (x, y - 0.057, z), (width - 0.12, 0.018, height - 0.12), screen, col, 0.012)
    for row in range(3):
        yy = y - 0.07
        zz = z - height * 0.27 + row * 0.18
        rod("Display signal " + str(row), (x - width * 0.36, yy, zz), (x + width * 0.33, yy, zz + (0.08 if row == 1 else -0.03)), 0.012, accent, col, 8)
    cylinder("Monitor stand", (x, y + 0.02, z - height * 0.56), 0.045, 0.24, frame, col)
    cube("Monitor foot", (x, y + 0.02, z - height * 0.72), (0.42, 0.28, 0.05), frame, col, 0.02)

def add_plant(col, x, y, z, accent):
    pot = material("Ceramic planter", (0.16, 0.19, 0.18, 1), 0.05, 0.6)
    leaf = material("Plant leaves", (0.12, 0.30, 0.22, 1), 0.0, 0.8)
    cylinder("Planter", (x, y, z + 0.22), 0.23, 0.42, pot, col)
    rod("Plant stem", (x, y, z + 0.4), (x, y, z + 1.15), 0.025, leaf, col)
    for index in range(5):
        angle = index * math.tau / 5.0
        sphere("Plant leaf", (x + math.cos(angle) * 0.22, y + math.sin(angle) * 0.16, z + 0.82 + (index % 2) * 0.12), (0.25, 0.10, 0.07), leaf, col, 16, 10)

def add_bookshelf(col, x, y, z, accent):
    wood = material("Walnut", (0.15, 0.085, 0.045, 1), 0.05, 0.36)
    cube("Bookcase back", (x, y, z + 1.45), (2.0, 0.16, 2.9), wood, col)
    for side in [-0.92, 0.92]:
        cube("Bookcase upright", (x + side, y - 0.02, z + 1.45), (0.12, 0.38, 2.95), wood, col)
    for shelf in range(5):
        zz = z + 0.22 + shelf * 0.58
        cube("Book shelf", (x, y - 0.03, zz), (1.95, 0.42, 0.09), wood, col)
        for book in range(7):
            bw = 0.12 + (book % 3) * 0.015
            bx = x - 0.78 + book * 0.23
            book_color = (0.18 + 0.05 * (book % 3), 0.13 + 0.03 * (book % 2), 0.09 + 0.04 * (shelf % 2), 1)
            book_mat = material("Book spine %d %d" % (shelf, book), book_color, 0.0, 0.7)
            cube("Archive book", (bx, y - 0.25, zz + 0.19), (bw, 0.18, 0.34 + 0.04 * (book % 2)), book_mat, col, 0.008)

def add_lamp(col, x, y, z, accent):
    brass = material("Brushed brass", (0.56, 0.39, 0.18, 1), 0.72, 0.26)
    shade = material("Warm lamp shade", (0.72, 0.57, 0.32, 1), 0.25, 0.34)
    cylinder("Lamp base", (x, y, z + 0.06), 0.19, 0.10, brass, col)
    rod("Lamp stem", (x, y, z + 0.10), (x, y, z + 0.62), 0.035, brass, col)
    sphere("Lamp shade", (x, y - 0.05, z + 0.72), (0.28, 0.25, 0.16), shade, col)

def add_globe(col, x, y, z, accent):
    globe_mat = material("Globe ocean", (0.045, 0.16, 0.22, 1), 0.12, 0.32)
    brass = material("Globe brass", (0.56, 0.40, 0.19, 1), 0.75, 0.25)
    sphere("World globe", (x, y, z + 0.7), (0.48, 0.48, 0.48), globe_mat, col)
    torus("Globe meridian", (x, y, z + 0.7), 0.53, 0.018, brass, col, (math.pi / 2, 0, 0))
    rod("Globe axis", (x, y, z + 0.12), (x, y, z + 1.22), 0.025, brass, col)
    cylinder("Globe foot", (x, y, z + 0.08), 0.26, 0.10, brass, col)

def add_screen_wall(col, accent, count=6):
    for index in range(count):
        row = index // 3
        column = index % 3
        add_monitor(col, -2.2 + column * 2.2, 2.55, 2.35 - row * 1.25, accent, 1.82, 0.92)

def add_glass_partition(col, x, y, z, height, accent):
    glass = material("Smoked glass", (0.07, 0.13, 0.16, 0.35), 0.15, 0.18)
    cube("Glass partition", (x, y, z + height / 2), (0.08, 0.08, height), glass, col, 0.01)
    brass = material("Accent trim " + str(accent), accent, 0.55, 0.3)
    cube("Glass trim", (x, y, z + height), (0.10, 0.12, 0.06), brass, col, 0.01)

def build_agent(faction, output_dir):
    agent_id = faction["id"]
    col = collection("Agent_" + agent_id)
    accent = material("Agent accent " + agent_id, faction["accent"], 0.45, 0.3)
    hair = material("Hair " + agent_id, faction["hair"], 0.02, 0.58)
    skin = material("Skin " + agent_id, faction["skin"], 0.0, 0.7)
    suit = material("Suit " + agent_id, faction["suit"], 0.12, 0.38)
    shirt = material("Shirt " + agent_id, faction["shirt"], 0.0, 0.55)
    dark = material("Facial detail " + agent_id, (0.045, 0.04, 0.04, 1), 0.0, 0.55)
    metal = material("Eyewear metal", (0.48, 0.40, 0.25, 1), 0.78, 0.22)

    cylinder("Bust plinth", (0, 0, 0.12), 0.55, 0.22, accent, col)
    sphere("Jacket torso", (0, 0, 0.86), (0.72, 0.40, 0.82), suit, col)
    sphere("Shoulder line", (0, 0.0, 1.22), (0.77, 0.37, 0.34), suit, col)
    cylinder("Neck", (0, 0, 1.57), 0.19, 0.42, skin, col)
    sphere("Shirt front", (0, -0.355, 1.02), (0.26, 0.06, 0.48), shirt, col)
    sphere("Head", (0, -0.015, 2.03), (0.43, 0.39, 0.55), skin, col)
    for side in [-1, 1]:
        sphere("Ear", (side * 0.42, -0.01, 1.98), (0.09, 0.10, 0.14), skin, col, 16, 10)
        sphere("Eye socket", (side * 0.155, -0.366, 2.08), (0.075, 0.035, 0.055), shirt, col, 16, 10)
        sphere("Eye", (side * 0.155, -0.395, 2.08), (0.032, 0.022, 0.032), dark, col, 16, 10)
        rod("Eyebrow", (side * 0.23, -0.39, 2.17), (side * 0.08, -0.405, 2.18), 0.018, hair, col, 10)
    sphere("Nose", (0, -0.405, 1.94), (0.075, 0.10, 0.12), skin, col, 16, 10)
    rod("Mouth", (-0.09, -0.377, 1.82), (0.09, -0.377, 1.82), 0.012, dark, col, 10)
    sphere("Hair cap", (0, 0.0, 2.34), (0.47, 0.40, 0.32), hair, col)
    sphere("Rear hair", (0, 0.22, 2.02), (0.46, 0.28, 0.48), hair, col)
    for side in [-1, 1]:
        sphere("Hair side lock", (side * 0.36, -0.03, 2.02), (0.12, 0.23, 0.38), hair, col)
        rod("Arm", (side * 0.50, 0.02, 1.20), (side * 0.66, -0.13, 0.50), 0.15, suit, col, 20)
        sphere("Cuff", (side * 0.66, -0.13, 0.51), (0.16, 0.16, 0.12), shirt, col)
    # Lapels and a faction-specific neck detail make the six silhouettes legible.
    for side in [-1, 1]:
        cube("Jacket lapel", (side * 0.19, -0.395, 1.30), (0.18, 0.06, 0.52), accent if agent_id == "trend" else suit, col, 0.025).rotation_euler[1] = side * -0.18
    if agent_id in ["value", "quant"]:
        for side in [-1, 1]:
            torus("Eyeglass rim", (side * 0.155, -0.424, 2.075), 0.105, 0.012, metal, col, (math.pi / 2, 0, 0))
        rod("Eyeglass bridge", (-0.05, -0.43, 2.075), (0.05, -0.43, 2.075), 0.012, metal, col)
    if agent_id == "value":
        sphere("Silver sideburn", (-0.35, 0.03, 2.14), (0.13, 0.22, 0.22), hair, col)
        sphere("Short beard", (0, -0.31, 1.72), (0.25, 0.12, 0.11), hair, col)
        cylinder("Gold tie pin", (0, -0.438, 1.12), 0.035, 0.06, accent, col, 16, (math.pi / 2, 0, 0))
    elif agent_id == "growth":
        for side in [-1, 1]:
            sphere("Long hair fall", (side * 0.34, 0.10, 1.72), (0.16, 0.24, 0.62), hair, col)
        sphere("Emerald collar", (0, -0.41, 1.42), (0.20, 0.05, 0.14), accent, col)
    elif agent_id == "trend":
        sphere("Swept hair", (0.06, -0.18, 2.40), (0.34, 0.28, 0.18), hair, col)
        torus("Headset arc", (0, 0.0, 1.52), 0.27, 0.035, accent, col, (math.pi / 2, 0, 0))
        sphere("Headset ear cup", (0.42, -0.01, 1.58), (0.09, 0.08, 0.15), accent, col)
    elif agent_id == "quant":
        sphere("Hair bun", (0.0, 0.30, 2.35), (0.18, 0.19, 0.20), hair, col)
        sphere("Violet collar", (0, -0.41, 1.42), (0.20, 0.05, 0.13), accent, col)
    elif agent_id == "sentiment":
        for side in [-1, 1]:
            sphere("Long hair", (side * 0.34, 0.11, 1.66), (0.16, 0.22, 0.72), hair, col)
        sphere("Amber scarf", (0, -0.43, 1.48), (0.33, 0.07, 0.13), accent, col)
    elif agent_id == "macro":
        sphere("Silver bob", (0, 0.03, 2.30), (0.49, 0.40, 0.39), hair, col)
        sphere("Cyan scarf", (0, -0.43, 1.46), (0.34, 0.07, 0.14), accent, col)
    path = os.path.join(output_dir, "agents", agent_id + ".glb")
    export_collection(col, path)
    return col

def build_room(faction, output_dir):
    agent_id = faction["id"]
    col = collection("Room_" + agent_id)
    accent = material("Room accent " + agent_id, faction["accent"], 0.5, 0.3)
    floor = material("Room floor", (0.055, 0.075, 0.085, 1), 0.18, 0.42)
    wall = material("Room wall", (0.075, 0.095, 0.11, 1), 0.08, 0.65)
    wood = material("Room walnut", (0.16, 0.095, 0.055, 1), 0.08, 0.4)
    metal = material("Room dark metal", (0.055, 0.07, 0.08, 1), 0.68, 0.3)
    leather = material("Room leather", (0.16, 0.095, 0.065, 1), 0.0, 0.7)
    cube("Room floor slab", (0, 0, -0.12), (12, 10, 0.24), floor, col, 0.02)
    cube("Room rear wall", (0, 3.9, 2.7), (12, 0.20, 5.4), wall, col, 0.03)
    cube("Room left wall", (-5.9, 0, 2.7), (0.20, 8, 5.4), wall, col, 0.03)
    cube("Room right wall", (5.9, 0, 2.7), (0.20, 8, 5.4), wall, col, 0.03)

    image_path = os.path.join(PROJECT_ROOT, "assets", "rooms-sprite.webp")
    backplate = image_material("Reference environment " + agent_id, image_path)
    backplate_plane = plane("Room cinematic backplate", (0, 3.78, 2.85), 11.2, 5.1, backplate, col)
    apply_atlas_uv(backplate_plane, int(faction["roomX"]), int(faction["roomY"]))

    # Main desk and the human-scale workstation.
    cube("Executive desk top", (0, -0.65, 1.06), (4.8, 1.55, 0.16), wood, col, 0.075)
    for x in [-2.05, 2.05]:
        for y in [-1.18, -0.12]:
            cube("Desk leg", (x, y, 0.48), (0.14, 0.14, 1.0), metal, col, 0.025)
    cube("Desk front fascia", (0, -1.39, 0.82), (3.2, 0.08, 0.34), metal, col, 0.02)
    cube("Desk accent inlay", (0, -1.445, 0.85), (1.2, 0.018, 0.025), accent, col, 0.004)

    # A chair sits behind the desk, ready for the Agent model.
    cylinder("Chair base", (0, 0.45, 0.18), 0.52, 0.12, metal, col)
    cylinder("Chair column", (0, 0.45, 0.48), 0.09, 0.52, metal, col)
    cube("Chair seat", (0, 0.45, 0.82), (1.15, 0.95, 0.22), leather, col, 0.12)
    cube("Chair back", (0, 0.88, 1.45), (1.10, 0.22, 1.18), leather, col, 0.14)

    add_monitor(col, -1.10, 0.18, 1.92, accent, 1.45, 0.88)
    add_monitor(col, 1.10, 0.18, 1.92, accent, 1.45, 0.88)
    cube("Desk keyboard", (0, -0.28, 1.17), (0.86, 0.28, 0.035), metal, col, 0.02)

    # Each room has a unique architectural signature.
    if agent_id == "value":
        add_bookshelf(col, -4.65, 2.4, 0.0, accent)
        add_lamp(col, 2.75, -0.55, 1.15, accent)
        cube("Archive side cabinet", (4.25, 1.8, 0.62), (1.2, 0.8, 1.2), wood, col)
    elif agent_id == "growth":
        add_glass_partition(col, -4.2, 1.0, 0.0, 3.6, accent)
        add_glass_partition(col, 4.2, 1.0, 0.0, 3.6, accent)
        add_plant(col, -3.8, -0.2, 0.0, accent)
        cube("Idea board", (3.7, 2.9, 2.5), (2.0, 0.12, 1.7), material("Whiteboard", (0.72, 0.76, 0.72, 1), 0.05, 0.5), col)
    elif agent_id == "trend":
        add_monitor(col, 0, 2.65, 3.0, accent, 3.6, 1.3)
        add_monitor(col, -3.5, 0.1, 2.2, accent, 1.2, 0.78)
        add_monitor(col, 3.5, 0.1, 2.2, accent, 1.2, 0.78)
    elif agent_id == "quant":
        for rack_x in [-4.4, 4.4]:
            cube("Compute rack", (rack_x, 2.4, 1.65), (0.75, 0.75, 3.3), metal, col, 0.05)
            for level in range(6):
                cube("Server bay", (rack_x, 1.99, 0.35 + level * 0.49), (0.58, 0.04, 0.34), accent, col, 0.02)
        add_monitor(col, 0, 2.8, 3.2, accent, 4.4, 1.1)
    elif agent_id == "sentiment":
        add_screen_wall(col, accent, 6)
        add_plant(col, 4.65, -0.4, 0.0, accent)
        cylinder("Round collaboration table", (0, 1.7, 0.92), 1.4, 0.12, wood, col)
    elif agent_id == "macro":
        add_monitor(col, 0, 2.7, 3.0, accent, 5.0, 1.45)
        add_globe(col, 3.8, 1.6, 0.0, accent)
        cube("Global briefing table", (-3.7, 1.5, 0.9), (1.5, 2.1, 0.16), wood, col)
    path = os.path.join(output_dir, "rooms", agent_id + ".glb")
    export_collection(col, path)
    return col

def build_banknote(output_dir):
    col = collection("Prop_Banknote")
    paper = material("Banknote paper", (0.48, 0.72, 0.53, 1), 0.08, 0.55)
    ink = material("Banknote ink", (0.12, 0.35, 0.23, 1), 0.15, 0.48)
    gold = material("Banknote foil", (0.82, 0.66, 0.36, 1), 0.7, 0.24)
    cube("Banknote body", (0, 0, 0), (1.25, 0.035, 0.68), paper, col, 0.035)
    cube("Banknote inner border", (0, -0.021, 0), (1.10, 0.008, 0.54), ink, col, 0.025)
    torus("Banknote seal", (0, -0.03, 0), 0.16, 0.018, gold, col, (math.pi / 2, 0, 0))
    for x in [-0.48, 0.48]:
        sphere("Banknote rosette", (x, -0.032, 0), (0.06, 0.012, 0.06), gold, col, 12, 8)
    path = os.path.join(output_dir, "banknote.glb")
    export_collection(col, path)
    return col

def export_collection(col, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    objects = list(col.objects)
    for obj in objects:
        obj.select_set(True)
    if objects:
        bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True)
    bpy.ops.object.select_all(action="DESELECT")

def parse_output_dir():
    raw = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args, _unknown = parser.parse_known_args(raw)
    return os.path.abspath(os.path.join(PROJECT_ROOT, args.output))

def main():
    output_root = parse_output_dir()
    source_dir = os.path.join(output_root, "source")
    generated_dir = os.path.join(output_root, "generated")
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(os.path.join(generated_dir, "agents"), exist_ok=True)
    os.makedirs(os.path.join(generated_dir, "rooms"), exist_ok=True)

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for col in list(bpy.data.collections):
        if col.name != "Collection":
            bpy.data.collections.remove(col)

    for faction in FACTIONS:
        build_agent(faction, generated_dir)
    for faction in FACTIONS:
        build_room(faction, generated_dir)
    build_banknote(generated_dir)

    for image in bpy.data.images:
        if image.source == "FILE" and not image.packed_file:
            try:
                image.pack()
            except Exception:
                pass

    blend_path = os.path.join(source_dir, "ai_arena_assets.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

    manifest = {
        "source": os.path.relpath(blend_path, PROJECT_ROOT),
        "blender_version": bpy.app.version_string,
        "agents": [os.path.relpath(os.path.join(generated_dir, "agents", faction["id"] + ".glb"), PROJECT_ROOT) for faction in FACTIONS],
        "rooms": [os.path.relpath(os.path.join(generated_dir, "rooms", faction["id"] + ".glb"), PROJECT_ROOT) for faction in FACTIONS],
        "props": [os.path.relpath(os.path.join(generated_dir, "banknote.glb"), PROJECT_ROOT)],
    }
    with open(os.path.join(generated_dir, "manifest.json"), "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
    print("AI ARENA BLENDER BUILD: 6 Agents, 6 rooms, 1 banknote, source saved to", blend_path)

if __name__ == "__main__":
    main()
