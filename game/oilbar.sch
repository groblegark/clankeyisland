/* Clanker City Chronicles — Scene 07: the Oil Bar, inside. */

room OilBarRoom {

    // story flags (cross-room state rides on inventory ownership or
    // common.sch globals — the rope gate keys on voltKey ownership in
    // midtown.scc; these stay room-local on purpose, see docs/NOTES.md)
    bit visitedOilBar;
    bit metSommelier;
    bit metAide;
    bit aideHinted;
    bit heardBoothToast;
    bit orderRound;     // 0 = the pour round, 1 = the billing round
    bit pourOrdered;
    bit aideServed;
    bit aideTalked;
    // "sommelier in cellar" is DERIVED: pourOrdered && !aideServed
    // (one less bit to desync — Scene 07 brief s3)

    object doorOut;
    object backBar;
    object sommelier;
    object oilBarCounter;
    object cellarList;
    object receiptSpike;
    object centrifuge;
    object aide;
    object boothAides;
    object portrait;
    object cellarHatch;
}
