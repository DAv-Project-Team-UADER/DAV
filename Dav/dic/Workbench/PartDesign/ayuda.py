def ayuda():
    print('Available commands in PartDesignWorkbench:')
    print('  base        - Subset: Body, NewSketch, Clone, SubShapeBinder')
    print('  additive    - Subset: additive features and primitives (Pad, Revolution, Box, Cone, etc.)')
    print('  subtractive - Subset: subtractive features and primitives (Pocket, Groove, Hole, etc.)')
    print('  modify      - Subset: shape modifiers (Fillet, Chamfer, Draft, Thickness, Boolean)')
    print('  transform   - Subset: patterns and transformations (LinearPattern, Mirrored, PolarPattern, etc.)')
    print('  manage      - Subset: tree management and preferences (MoveFeature, MoveTip, Preferences, etc.)')

    print('\nGeneral Precondition:')
    print('  Most commands require an active Body. Additive/subtractive operations and transformations')
    print('  also require a previously selected sketch or model features/edges.')
