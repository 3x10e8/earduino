/*
  This example reads audio data from the on-board PDM microphones, and prints
  out the samples to the Serial console. The Serial Plotter built into the
  Arduino IDE can be used to plot the audio data (Tools -> Serial Plotter)

  Circuit:
  - Arduino Nano 33 BLE board or
  - Arduino Portenta H7 board plus Portenta Vision Shield

  This example code is in the public domain.
*/

#include <PDM.h>

// number of output channels
static const char channels = 2;

// PDM output frequency
static const int frequency = 32000;
// Options from PDM example sketch:
// - 16 kHz sample rate for the Arduino Nano 33 BLE Sense
// - 32 kHz or 64 kHz sample rate for the Arduino Portenta Vision Shield

// PDM output frequency
static const int bufferTime_s = 1; // duration of audio capture to buffer (seconds)

// Buffer to read samples into, each sample is 16-bits
short sampleBuffer[frequency*bufferTime_s*2*2]; // a second of stereo data (2 bytes/sample)
//short sampleBuffer[4096]; //experiment to see if a shorter buffer allows easier streaming over serial, not sure.

// Number of audio samples read
volatile int samplesRead;

void setup() {
  // initialize RGB LEDs as outputs
  pinMode(LEDR, OUTPUT); // high when outside of mic ISR
  pinMode(LEDB, OUTPUT); // high outside of serial writing

  Serial.begin(115200, SERIAL_8N1); // SERIAL_8N1 is default, this is just for clarity
  while (!Serial);

  // Configure the data receive callback
  PDM.onReceive(onPDMdata);

  // Optionally set the gain
  // Defaults to 20 on the BLE Sense and -10 on the Portenta Vision Shield
  PDM.setGain(0);

  // Initialize PDM with:
  // - two channels (stereo mode)
  // - 32kHz sample rate
  if (!PDM.begin(channels, frequency)) {
    Serial.println("Failed to start PDM!");
    while (1);
  }
}

void loop() {
  // Wait for samples to be read
  if (samplesRead) {
    digitalWrite(LEDB, LOW); 

    // Print samples to the serial monitor or plotter
    for (int i = 0; i < samplesRead; i++) {
      if(channels == 2) {
        Serial.write(sampleBuffer[i]);
        i++;
      }
      Serial.write(sampleBuffer[i]);
    }

    // Clear the read count
    samplesRead = 0;
    
    digitalWrite(LEDB, HIGH); 
  }
}

/**
 * Callback function to process the data from the PDM microphone.
 * NOTE: This callback is executed as part of an ISR.
 * Therefore using `Serial` to print messages inside this function isn't supported.
 * */
void onPDMdata() {
  // turn off LED
  digitalWrite(LEDR, LOW);   

  // Query the number of available bytes
  int bytesAvailable = PDM.available();

  // Read into the sample buffer
  PDM.read(sampleBuffer, bytesAvailable);

  // 16-bit, 2 bytes per sample
  samplesRead = bytesAvailable / 2;

  // turn on LED
  digitalWrite(LEDR, HIGH); 
}
