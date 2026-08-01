#!/usr/bin/env python
"""Wrapper para ejecutar el proyecto Django desde la raíz del repositorio."""

import os
import runpy
import sys


if __name__ == "__main__":
    project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend_data_server")
    os.chdir(project_dir)
    sys.path.insert(0, project_dir)
    runpy.run_path(os.path.join(project_dir, "manage.py"), run_name="__main__")
