/* Clanker City Chronicles — Scene 09: the Rustlers' hideout (Act 3). */

room HideoutRoom {

    // story flags (cross-scene recovery rides on these bits AND on
    // getObjectOwner(InventoryItems::windupKey) == VAR_EGO; keyRecovered
    // is kept as its own bit because scenes 10-11 consume the keys at the
    // Dynamo and must still know the recovery happened after the owner
    // changes -- the owner==VAR_EGO pitfall, docs/NOTES.md).
    bit denEntered;        // front entry cutscene played
    bit loftEntered;       // hatch eavesdrop played
    bit ransomKnown;       // set by EITHER entry beat; gates steal + parley
    bit arithmeticLanded;  // parley stage 1 won
    bit keyRecovered;      // either route (EXPORTED to Scene 10/11)
    bit keyByParley;       // EXPORTED: the wind-up crew is contracted
    bit keyByTheft;        // EXPORTED: crew arrives uncontracted
    bit ejectedOnce;       // magnet flop happened (retry flavor line)
    bit metSlotEye;        // first slot-eye TalkTo done
    bit metTable;          // first card-table TalkTo done

    char* dlgStr;          // dialog-option scratch (the openquest idiom)

    object doorTavern;
    object doorStation;
    object slotEye;
    object stove;
    object framedNotice;
    object cardTable;
    object keyOnLine;
    object ransomDesk;
    object capstan;
    object trophyWall;
    object doorAlley;
    object hatch;
    object loftCleat;
    object loftShutter;
}
