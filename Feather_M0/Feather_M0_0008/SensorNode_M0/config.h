/*
*	Project ID, Location ID, and device address will have to be added to the database before 
* 		these values can be changed.
*	Device address will also have to be added to the network server forward list
*		Available Device addresses are 0x00540006, 0x00540008 and 0x00540008
*/

#define PROJID 8

#define LOCID 1 //This time it's composite rubber

#ifndef DEVADDR
#define DEVADDR 0x00540008
#endif

#ifndef TX_INTERVAL
#define TX_INTERVAL 120
#endif
