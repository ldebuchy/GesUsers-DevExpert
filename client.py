
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.controller.exec import *

cli = Console()
cli.set_menu(lambda: cli.start_menu())