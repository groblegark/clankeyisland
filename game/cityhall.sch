/* Clanker City Chronicles — Scene 08: City Hall / Mayor Piston. */

room CityHallRoom {

    // story flags (cross-room state rides on inventory ownership or
    // common.sch globals; these stay room-local on purpose — see
    // docs/NOTES.md. pistonCracked is kept as its own bit so adjacent
    // rooms can test the crack cheaply without reading pistonRound.)
    bit visitedCityHall;
    int pistonRound;     // 0 none / 1 / 2 / 3 / 4 cracked
    bit pistonCracked;   // == (pistonRound 4); EXPORTED to Scene 09
    bit act3Started;     // set at the close of the confession; EXPORTED:
                         // gates Scene 09's door + alley/loft addenda
    bit posterVoided;
    bit curtainsOpen;
    bit metCaliper;      // first TalkTo done; second+ fires the R3 plant

    object doorOut;
    object caliper;
    object aideDesk;
    object portraits;
    object bannerStack;
    object windowDynamo;
    object gauge;
    object mayorDesk;
    object piston;
}
