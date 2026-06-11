/* Clanker City Chronicles — shared declarations.
 * Framework derived from ScummC's openquest example,
 * Copyright (C) 2007 Alban Bedel (GPL v2+). Game content (C) 2026.
 */

// The action verbs
verb Give,  PickUp, Use;
verb Open,  LookAt, Smell;
verb TalkTo,Move;

verb WalkTo, WalkToXY;

verb UsedWith;
verb InventoryObject;

bit verbsOn,cursorOn,cursorLoaded;
int sntcVerb,sntcObjA,sntcObjADesc,sntcObjB,sntcObjBDesc;
int* invObj;

// The sentence line
verb SntcLine;

// The inventory slots
verb invSlot0 @ 100, invSlot1 @ 101, invSlot2 @ 102, invSlot3 @ 103,
    invSlot4 @ 104, invSlot5 @ 105, invSlot6 @ 106, invSlot7 @ 107;

// The inventory arrows
verb invUp, invDown;
int invOffset;
#define INVENTORY_COL   2
#define INVENTORY_LINE  2
#define INVENTORY_SLOTS (INVENTORY_COL*INVENTORY_LINE)

// The verb colors — indices into the master palette (tools/genassets.py)
#define VERB_COLOR       100
#define VERB_HI_COLOR    101
#define VERB_DIM_COLOR   102
#define VERB_BACK_COLOR  103
#define WHITE_COLOR      104

// Object callbacks
verb Icon,Preposition,SetBoxes;

// Object class
class Openable,Pickable, Person;

// Allow the objects to insert a word (like "to" or "with") between the
// verb and object in the sentence.
char *sntcPrepo;

// List of the objects used to handle action on actors
int  *actorObject;

// define actors
actor sprocket;
#define SPROCKET_COLOR  105
#define BETTY_COLOR     106

room ResRoom {

    // our standard charset
    chset chtest;
    // dialog charset
    chset dialogCharset;

    script inputHandler(int area,int cmd, int btn);
    script keyboardHandler(int key);
    script inventoryHandler(int obj);
    script showCursor();
    script hideCursor();
    script mouseWatch();
    script defaultAction(int vrb, int objA, int objB);

    script quit();
}
