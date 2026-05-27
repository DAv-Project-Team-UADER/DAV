# SPDX-License-Identifier: LGPL-2.1-or-later
# DAV workbench (Python): copied from DAV-Luigi/Dav at build time.

if(NOT BUILD_GUI)
    return()
endif()

set(DAV_MOD_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../../../../Dav")

if(NOT EXISTS "${DAV_MOD_SOURCE_DIR}/InitGui.py")
    message(WARNING "DAV mod sources not found at ${DAV_MOD_SOURCE_DIR}")
    return()
endif()

add_custom_target(
    DAV_ModCopy ALL
    COMMAND
        "${CMAKE_COMMAND}" -E rm -rf "${CMAKE_BINARY_DIR}/Mod/DAV"
    COMMAND
        "${CMAKE_COMMAND}" -E copy_directory "${DAV_MOD_SOURCE_DIR}" "${CMAKE_BINARY_DIR}/Mod/DAV"
    COMMENT "Copying DAV workbench into ${CMAKE_BINARY_DIR}/Mod/DAV"
)

install(
    DIRECTORY "${DAV_MOD_SOURCE_DIR}/"
    DESTINATION Mod/DAV
    FILES_MATCHING
    PATTERN "*.py"
    PATTERN "*.md"
)
