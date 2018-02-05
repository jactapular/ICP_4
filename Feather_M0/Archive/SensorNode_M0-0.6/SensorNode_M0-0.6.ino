  /*******************************************************************************
 * Modified by Thomas Laurenson, 2017
 * Specific modifications for use of Dragino LoRaSHield on AU915, sub-band 2
 *
 * Copyright (c) 2015 Thomas Telkamp and Matthijs Kooijman
 *
 * Permission is hereby granted, free of charge, to anyone
 * obtaining a copy of this document and accompanying files,
 * to do whatever they want with them without any restriction,
 * including, but not limited to, copying, modification and redistribution.
 * NO WARRANTY OF ANY KIND IS PROVIDED.
 *
 * This example sends a valid LoRaWAN packet with payload "Hello,
 * world!", using frequency and encryption settings matching those of
 * the (early prototype version of) The Things Network.
 *
 * Note: LoRaWAN per sub-band duty-cycle limitation is enforced (1% in g1,
 *  0.1% in g2).
 *
 * Change DEVADDR to a unique address!
 * See http://thethingsnetwork.org/wiki/AddressSpace
 *
 * Do not forget to define the radio type correctly in config.h.
 *
 *******************************************************************************/
#include <lmic.h>
#include <hal/hal.h>
#include <Wire.h>
#include <SI7021.h>
#include <SPI.h>
#include <OneWire.h> 
#include <DallasTemperature.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>
#include "config.h"

// LoRaWAN NwkSKey, network session key
// This is the default Semtech key, which is used by the prototype TTN
// network initially.
static const PROGMEM u1_t NWKSKEY[16] = { 0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6, 0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF, 0x4F, 0x3C };

// LoRaWAN AppSKey, application session key
// This is the default Semtech key, which is used by the prototype TTN
// network initially.
static const u1_t PROGMEM APPSKEY[16] = { 0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6, 0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF, 0x4F, 0x3C };

// LoRaWAN end-device address (DevAddr)
// See http://thethingsnetwork.org/wiki/AddressSpace https://www.thethingsnetwork.org/wiki/LoRaWAN/Address-Space
//static const u4_t DEVADDR = 0x00540006; Define in config file

// These callbacks are only used in over-the-air activation, so they are
// left empty here (we cannot leave them out completely unless
// DISABLE_JOIN is set in config.h, otherwise the linker will complain).

void os_getArtEui (u1_t* buf) { }
void os_getDevEui (u1_t* buf) { }
void os_getDevKey (u1_t* buf) { }

//static uint8_t mydata[] = "Hello, world!?";
//Standard format for server to recieve for up to 8 sensors
uint8_t mydata[14] = {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};



static osjob_t sendjob;

// Schedule TX every this many seconds (might become longer due to duty
// cycle limitations).
//const unsigned TX_INTERVAL = 60; Define in config.h

// Pin mapping
const lmic_pinmap lmic_pins = {
    .nss = 8,  
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 4,
    .dio = {3,5,6},
};

/********************************************************************/
/*                  Waterproof Sensor Setup                         */
/********************************************************************/

// Data wire is plugged into pin 12 on the Arduino 
#define ONE_WIRE_BUS 12
/********************************************************************/
// Setup a oneWire instance to communicate with any OneWire devices  
// (not just Maxim/Dallas temperature ICs) 
OneWire oneWire(ONE_WIRE_BUS); 
/********************************************************************/
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);
/********************************************************************/ 


/********************************************************************/
/*                      LUX Sensor Setup                            */
/********************************************************************/
Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);



void onEvent (ev_t ev) {
    //Serial.print(os_getTime());
    //Serial.print(": ");
    switch(ev) {
        case EV_SCAN_TIMEOUT:
            //Serial.println(F("EV_SCAN_TIMEOUT"));
            break;
        case EV_BEACON_FOUND:
            //Serial.println(F("EV_BEACON_FOUND"));
            break;
        case EV_BEACON_MISSED:
            //Serial.println(F("EV_BEACON_MISSED"));
            break;
        case EV_BEACON_TRACKED:
            //Serial.println(F("EV_BEACON_TRACKED"));
            break;
        case EV_JOINING:
            //Serial.println(F("EV_JOINING"));
            break;
        case EV_JOINED:
            //Serial.println(F("EV_JOINED"));
            break;
        case EV_RFU1:
            //Serial.println(F("EV_RFU1"));
            break;
        case EV_JOIN_FAILED:
            //Serial.println(F("EV_JOIN_FAILED"));
            break;
        case EV_REJOIN_FAILED:
            //Serial.println(F("EV_REJOIN_FAILED"));
            break;
            break;
        case EV_TXCOMPLETE:
            //Serial.println(F("EV_TXCOMPLETE (includes waiting for RX windows)"));
            if(LMIC.dataLen) {
                // data received in rx slot after tx
                //Serial.print(F("Data Received: "));
                //Serial.write(LMIC.frame+LMIC.dataBeg, LMIC.dataLen);
                //Serial.println();
            }
            // Schedule next transmission
            digitalWrite(13, LOW); 
            os_setTimedCallback(&sendjob, os_getTime()+sec2osticks(TX_INTERVAL), do_send);
            break;
        case EV_LOST_TSYNC:
            //Serial.println(F("EV_LOST_TSYNC"));
            break;
        case EV_RESET:
            //Serial.println(F("EV_RESET"));
            break;
        case EV_RXCOMPLETE:
            // data received in ping slot
            //Serial.println(F("EV_RXCOMPLETE"));
            break;
        case EV_LINK_DEAD:
            //Serial.println(F("EV_LINK_DEAD"));
            break;
        case EV_LINK_ALIVE:
            //Serial.println(F("EV_LINK_ALIVE"));
            break;
         default:
            //Serial.println(F("Unknown event"));
            break;
    }
}

void do_send(osjob_t* j){
    // Check if there is not a current TX/RX job running
    if (LMIC.opmode & OP_TXRXPEND) {
        //Serial.println(F("OP_TXRXPEND, not sending"));
        //Serial.print("OP_TXRXPEND, not sending; at freq: ");
        //Serial.println(LMIC.freq);        
    } else {
        uint16_t int_temp, int_lux;
        // Prepare upstream data transmission at the next possible time.
        //LMIC_setTxData2(1, mydata, sizeof(mydata)-1, 0);
        digitalWrite(13, HIGH); 
        sensors.requestTemperatures(); // Send the command to get temperature readings  
        
        /********************************************************************/
        /*                         WP Temp sensor                           */
        int_temp = (uint16_t)(sensors.getTempCByIndex(0)*100);
        //Serial.print("Temperature is: "); 
        //Serial.println(int_temp/100);
        
        mydata[2] = (uint8_t)(int_temp >> 8);
        mydata[3] = (uint8_t)(int_temp & 0xFF);
        
        
        /*temp = (mydata[0] << 8 | mydata[1]);    
        Serial.print("Temperature from uint8_t array: "); 
        Serial.println(temp/100);
        */
        //Serial.println("");
        /********************************************************************/
        /*                         LUX Sensor                               */
        sensors_event_t event;
        tsl.getEvent(&event);
       
        /* Display the results (light is measured in lux) */
        if (event.light)
        {
          /*
          Serial.print("Lux is :"); 
          Serial.println(event.light); 
          Serial.println("");*/
          int_lux = (event.light);
          mydata[4] = (uint8_t)(int_lux >> 8);
          mydata[5] = (uint8_t)(int_lux & 0xFF);
        }
        else
        {
          /* If event.light = 0 lux the sensor is probably saturated
             and no reliable data could be generated! */
          //Serial.println("Sensor overload");
        }
        
        //mydata[0]=data.celsiusHundredths/100;
        //mydata[1]=data.humidityBasisPoints/100;
       
       LMIC_setTxData2(1, mydata, sizeof(mydata), 0); 
          
        
        //Serial.println(mydata[0]);
        //Serial.print(F("Packet queued for freq: "));
        //Serial.println(LMIC.freq);
    }
    // Next TX is scheduled after TX_COMPLETE event.
}

void setup() {
    //Serial.begin(9600);
    //while (!Serial);
    //Serial.println(F("Starting"));
    pinMode(13, OUTPUT);           // set pin to input
        
    sensors.begin();

    //Set Project ID
    mydata[0] = PROJID;
    //Set Location ID
    mydata[1] = LOCID;
    
    // LMIC init
    os_init();
    // Reset the MAC state. Session and pending data transfers will be discarded.
    LMIC_reset();

    // Set static session parameters. Instead of dynamically establishing a session
    // by joining the network, precomputed session parameters are be provided.
    #ifdef PROGMEM
    // On AVR, these values are stored in flash and only copied to RAM
    // once. Copy them to a temporary buffer here, LMIC_setSession will
    // copy them into a buffer of its own again.
    uint8_t appskey[sizeof(APPSKEY)];
    uint8_t nwkskey[sizeof(NWKSKEY)];
    memcpy_P(appskey, APPSKEY, sizeof(APPSKEY));
    memcpy_P(nwkskey, NWKSKEY, sizeof(NWKSKEY));
    LMIC_setSession (0x1, DEVADDR, nwkskey, appskey);
    #else
    // If not running an AVR with PROGMEM, just use the arrays directly 
    LMIC_setSession (0x1, DEVADDR, NWKSKEY, APPSKEY);
    #endif

    // THIS IS WHERE THE AUSTRALIA FREQUENCY MAGIC HAPPENS!
    // The frequency plan is hard-coded
    // But the band (or selected 8 channels) is configured here!
    // This is the same AU915 band as used by TTN
    
    // First, disable channels 8-16
    for (int channel=8; channel<16; ++channel) {
      LMIC_disableChannel(channel);
    }
    // Now, disable channels 16-72 (is there 72 ??)
    for (int channel=16; channel<72; ++channel) {
       LMIC_disableChannel(channel);
    }
    // This means only channels 8-15 are up

    // Disable link check validation
    LMIC_setLinkCheckMode(0);
    LMIC_setAdrMode(0);
    // Set data rate and transmit power (note: txpow seems to be ignored by the library)
    LMIC_setDrTxpow(DR_SF7,20);

    // Start job
    do_send(&sendjob);
}

void loop() {
    os_runloop_once();
    
}
