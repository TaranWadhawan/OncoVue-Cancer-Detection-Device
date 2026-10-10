#include <Servo.h>

Servo servo1;
Servo servo2;

int angle1 = 90;
int angle2 = 90;

const int LIMIT_S1_MIN = 2;
const int LIMIT_S1_MAX = 3;
const int LIMIT_S2_MIN = 4;
const int LIMIT_S2_MAX = 5;
const int ENCODER_CLK = 9;
const int ENCODER_DT = 8;
const int ENCODER_SW = 7;
const int LIGHT_PIN = 12;

int last_clk_state;
int light_intensity = 128;

void setup()
{
    Serial.begin(9600);

    servo1.attach(10);
    servo2.attach(11);

    servo1.write(angle1);
    servo2.write(angle2);

    pinMode(LIMIT_S1_MIN, INPUT_PULLUP);
    pinMode(LIMIT_S1_MAX, INPUT_PULLUP);
    pinMode(LIMIT_S2_MIN, INPUT_PULLUP);
    pinMode(LIMIT_S2_MAX, INPUT_PULLUP);

    pinMode(ENCODER_CLK, INPUT);
    pinMode(ENCODER_DT, INPUT);
    pinMode(ENCODER_SW, INPUT_PULLUP);
    pinMode(LIGHT_PIN, OUTPUT);

    analogWrite(LIGHT_PIN, light_intensity);
    last_clk_state = digitalRead(ENCODER_CLK);

    delay(500);
    Serial.println("System Ready: Dual Servo & Light Controller Active.");
}

void loop()
{
    int current_clk_state = digitalRead(ENCODER_CLK);
    if (current_clk_state != last_clk_state && current_clk_state == LOW)
    {
        if (digitalRead(ENCODER_DT) != current_clk_state)
        {
            light_intensity = constrain(light_intensity + 15, 0, 255);
        }
        else
        {
            light_intensity = constrain(light_intensity - 15, 0, 255);
        }
        analogWrite(LIGHT_PIN, light_intensity);
        Serial.print("LIGHT_VAL: ");
        Serial.println(light_intensity);
    }
    last_clk_state = current_clk_state;

    if (digitalRead(ENCODER_SW) == LOW)
    {
        delay(50);
        if (digitalRead(ENCODER_SW) == LOW)
        {
            light_intensity = (light_intensity > 0) ? 0 : 255;
            analogWrite(LIGHT_PIN, light_intensity);
            Serial.print("LIGHT_VAL: ");
            Serial.println(light_intensity);
            while (digitalRead(ENCODER_SW) == LOW)
                ;
        }
    }

    if (Serial.available() > 0)
    {
        String input = Serial.readStringUntil('\n');
        input.trim();

        if (input.length() > 0)
        {
            if (input.startsWith("light "))
            {
                int val = input.substring(6).toInt();
                light_intensity = constrain(val, 0, 255);
                analogWrite(LIGHT_PIN, light_intensity);
                Serial.print("LIGHT_VAL: ");
                Serial.println(light_intensity);
            }
            else
            {
                int space1 = input.indexOf(' ');
                if (space1 != -1)
                {
                    String servo_id = input.substring(0, space1);
                    int space2 = input.indexOf(' ', space1 + 1);

                    if (space2 != -1)
                    {
                        String direction = input.substring(space1 + 1, space2);
                        String deg_str = input.substring(space2 + 1);
                        int degrees = deg_str.toInt();

                        if (servo_id == "s1")
                        {
                            if (direction == "left")
                            {
                                if (digitalRead(LIMIT_S1_MIN) == HIGH)
                                {
                                    angle1 = constrain(angle1 - degrees, 0, 180);
                                    servo1.write(angle1);
                                    Serial.print("S1_POS: ");
                                    Serial.print(angle1);
                                    Serial.println(" deg");
                                }
                                else
                                {
                                    Serial.println("[Arduino Alert]: S1 Min limit reached! Blocked left rotation.");
                                }
                            }
                            else if (direction == "right")
                            {
                                if (digitalRead(LIMIT_S1_MAX) == HIGH)
                                {
                                    angle1 = constrain(angle1 + degrees, 0, 180);
                                    servo1.write(angle1);
                                    Serial.print("S1_POS: ");
                                    Serial.print(angle1);
                                    Serial.println(" deg");
                                }
                                else
                                {
                                    Serial.println("[Arduino Alert]: S1 Max limit reached! Blocked right rotation.");
                                }
                            }
                        }
                        else if (servo_id == "s2")
                        {
                            if (direction == "left")
                            {
                                if (digitalRead(LIMIT_S2_MIN) == HIGH)
                                {
                                    angle2 = constrain(angle2 - degrees, 0, 180);
                                    servo2.write(angle2);
                                    Serial.print("S2_POS: ");
                                    Serial.print(angle2);
                                    Serial.println(" deg");
                                }
                                else
                                {
                                    Serial.println("[Arduino Alert]: S2 Min limit reached! Blocked down rotation.");
                                }
                            }
                            else if (direction == "right")
                            {
                                if (digitalRead(LIMIT_S2_MAX) == HIGH)
                                {
                                    angle2 = constrain(angle2 + degrees, 0, 180);
                                    servo2.write(angle2);
                                    Serial.print("S2_POS: ");
                                    Serial.print(angle2);
                                    Serial.println(" deg");
                                }
                                else
                                {
                                    Serial.println("[Arduino Alert]: S2 Max limit reached! Blocked up rotation.");
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}