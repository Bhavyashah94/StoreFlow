import os
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtCore import QLibraryInfo
import os

# Print available drivers
print("Available SQL Drivers:", QSqlDatabase.drivers())

# Print the actual path where Qt is looking for SQL plugins
plugin_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
sql_driver_path = os.path.join(plugin_path, "sqldrivers")
print("Qt SQL Driver Path:", sql_driver_path)

print("Existing SQL Driver Files:", os.listdir(sql_driver_path) if os.path.exists(sql_driver_path) else "Not Found!")



