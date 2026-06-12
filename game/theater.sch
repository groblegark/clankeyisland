/* Clanker City Chronicles — Scene 05: inside the Grand Cog. */

room TheaterRoom {

    // story flags (cross-room state rides on inventory ownership:
    // getObjectOwner(x) == VAR_EGO — see docs/NOTES.md)
    bit visitedTheater;
    bit metEmcee;
    bit spotAwake;
    bit wonShow;

    object doorLobby;
    object spotBooth;
    object chandelier;
    object audience;
    object emcee;
    object stage;
    object backstageDoor;
}
