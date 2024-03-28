#include "max6675.h"

// Define the Arduino pins for the first MAX6675 module
int SO_PIN_1 = 11;  // Serail Out (SO) pin for the first module
int CS_PIN_1 = 12;  // Chip Select (CS) pin for the first module
int SCK_PIN_1 = 13; // Clock (SCK) pin for the first module

// Define the Arduino pins for the second MAX6675 module
int SO_PIN_2 = 4;  // Serail Out (SO) pin for the second module
int CS_PIN_2 = 5;  // Chip Select (CS) pin for the second module
int SCK_PIN_2 = 13; // Clock (SCK) pin for the second module

// Define the Arduino pins for the second MAX6675 module
int SO_PIN_3 = 6;  // Serail Out (SO) pin for the second module
int CS_PIN_3 = 7;  // Chip Select (CS) pin for the second module
int SCK_PIN_3 = 13; // Clock (SCK) pin for the second module


// Define the Arduino pins for the second MAX6675 module
int SO_PIN_4 = 8;  // Serail Out (SO) pin for the second module
int CS_PIN_4 = 9;  // Chip Select (CS) pin for the second module
int SCK_PIN_4 = 13; // Clock (SCK) pin for the second module
// Create instances of the MAX6675 class for each module
MAX6675 thermocouple1(SCK_PIN_1, CS_PIN_1, SO_PIN_1);
MAX6675 thermocouple2(SCK_PIN_2, CS_PIN_2, SO_PIN_2);
MAX6675 thermocouple3(SCK_PIN_3, CS_PIN_3, SO_PIN_3);
MAX6675 thermocouple4(SCK_PIN_4, CS_PIN_4, SO_PIN_4);

void setup() {
  Serial.begin(9600);
  delay(500);
}

void loop() {
  // Read the current temperatures from both modules and print them to the serial monitor

  // Read the temperature from the first module in Celsius
  Serial.print("Temperature 1: ");
  Serial.print(thermocouple1.readCelsius());
  Serial.print("\xC2\xB0"); // shows degree symbol
  Serial.print("C  |  ");

  // Read the temperature from the second module in Celsius
  Serial.print("Temperature 2: ");
  Serial.print(thermocouple2.readCelsius());
  Serial.print("\xC2\xB0"); // shows degree symbol
  Serial.println("C");

  delay(1000);
}
