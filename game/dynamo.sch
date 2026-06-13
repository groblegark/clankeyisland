/* Clanker City Chronicles -- Scene 10: Dynamo District / Old Crank.
 * The twist scene: Key #3 turns out to be a person (Old Crank). The
 * player leaves holding all three keys, the Dynamo's three-slot interface
 * learned, ready for the Scene 11 rewind.
 *
 * Cross-room state rides on inventory ownership where it can (the docks
 * convention). crankGiven is kept as its own EXPORTED bit so Scene 11 can
 * test "the set is complete" cheaply; allThreeKeys mirrors it as the named
 * finale gate. Key #3 itself is InventoryItems::crankKey (ownership ==
 * VAR_EGO once picked up at the give).
 */

room DynamoRoom {

    bit visitedDynamoDistrict;
    bit heardGateHint;     // first gate contact done (setup + Crank's nudge)
    bit gateWound;         // the governor matched, turnstile released
    bit metCrank;          // first TalkTo with Old Crank
    bit dynamoPrimed;      // the dry run fired (two keys -> half-step lift)
    bit crankRevealed;     // Crank is Key #3, earned (any route)
    bit crankGiven;        // EXPORTED to Scene 11: Crank gave his key, wound down
    bit allThreeKeys;      // EXPORTED to Scene 11: the set is complete

    object wayDown;
    object fence;
    object plaque;
    object gate;
    object governor;
    object oldCrank;
    object workbench;
    object dynamo;
    object overlook;
}
