#include <Wire.h>
#include "BMI088.h"

float ax = 0, ay = 0, az = 0;
float gx = 0, gy = 0, gz = 0;
int16_t temp = 0;

BMI088 bmi088(BMI088_ACC_ADDRESS, BMI088_GYRO_ADDRESS);

// Complementary filter variables
float roll = 0.0;
float pitch = 0.0;

unsigned long lastTime = 0;

const float alpha = 0.98;  // Gyro weight

void setup() {
    Wire.begin();
    Serial.begin(115200);

    while (!Serial);

    Serial.println("BMI088 Roll/Pitch");

    while (1) {
        if (bmi088.isConnection()) {
            bmi088.initialize();
            Serial.println("BMI088 is connected");
            break;
        } else {
            Serial.println("BMI088 is not connected");
        }

        delay(2000);
    }

    // Read initial sensor values
    bmi088.getAcceleration(&ax, &ay, &az);

    // Initialize roll and pitch from accelerometer
    roll = atan2(ay, az) * 180.0 / PI;
    pitch = atan2(-ax, sqrt(ay * ay + az * az)) * 180.0 / PI;

    lastTime = millis();
}

void loop() {
    // Read sensors
    bmi088.getAcceleration(&ax, &ay, &az);
    bmi088.getGyroscope(&gx, &gy, &gz);

    // Calculate elapsed time
    unsigned long currentTime = millis();
    float dt = (currentTime - lastTime) / 1000.0f;
    lastTime = currentTime;

    // Accelerometer angles
    float rollAcc = atan2(ay, az) * 180.0 / PI;
    float pitchAcc = atan2(-ax, sqrt(ay * ay + az * az)) * 180.0 / PI;

    // Integrate gyro rates
    roll += gx * dt;
    pitch += gy * dt;

    // Complementary filter
    roll = alpha * roll + (1.0f - alpha) * rollAcc;
    pitch = alpha * pitch + (1.0f - alpha) * pitchAcc;

    // Output CSV format
    Serial.print(roll, 2);
    Serial.print(",");
    Serial.println(pitch, 2);

    delay(10);
}