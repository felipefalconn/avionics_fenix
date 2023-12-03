// This file is part of the Colibrino project.

// Colibrino is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// Colibrino is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with Foobar.  If not, see <https://www.gnu.org/licenses/>.

#include <Wire.h>
#include "MahonyAHRS.h"
#include "mpu6050.h"
#include "mouseIMU.h"
#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
//---------------------------------------------------------------------------------------------------
//Definitions
//Mouse

/*********************************************************************
 * Global variables
 */

//float ax_filtro, ay_filtro, az_filtro, gx_filtro, gy_filtro, gz_filtro;
bool conectado = false;
//float yaw_filtro, pitch_filtro, roll_filtro;
const int MPU_addr = 0x68;  // I2C address of the MPU-6050
/*********************************************************************
 * External ariables
 */
extern int AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;
extern float yaw_mahony, pitch_mahony, roll_mahony;
extern float axR, ayR, azR, gxR, gyR, gzR;
extern float axg, ayg, azg, gxrs, gyrs, gzrs;
extern bool g_novaPiscada;

extern int g_clique;

BluetoothSerial SerialBT;

#define I2C_SDA 32
#define I2C_SCL 33

 typedef struct {
  float value;
  float offset;
  float zero;
} EulerAngle;

void initializeEulerAngle(EulerAngle *angle) {
  angle->value = 0;
  angle->offset = 0;
  angle->zero = 0;
}

float corrigeAngulo(EulerAngle *angle) {
  static float sinalCorrigido = 0;
  float valorDeriv = (angle->value - angle->zero);
  angle->zero = angle->value;

  if (valorDeriv <= -180) {
    angle->offset += +360.0f;
  } else if (valorDeriv >= 180) {
    angle->offset += -360.0f;
  }
  sinalCorrigido = angle->value;
  sinalCorrigido += angle->offset;

  return sinalCorrigido;
}

void setup() 
{
  Wire.begin(I2C_SDA,I2C_SCL);
  Wire.setClock(100000);  // 400kHz I2C clock. Comment this line if having compilation difficulties
  delay(100);
  MPU6050_Init();
  Serial.begin(115200);
  SerialBT.begin("ESP32test"); //Bluetooth device name

  // pinMode(ACIONADOR,INPUT);
  // eyeBlinkSetup();
}


void loop() 
{
  static int printDivider = 10;
  static int estado = 0;
  int xchg = 0, ychg = 0;
  int scroll = 0;
  bool estadoAcionador = false;
  static int contador = 0;
  static int counter = 0;
  static int subcounter = 10;


  // eyeBlinkRefresh();
  mpu6050_GetData();
  filtraIMU();
 


  if(IMU_calibration())
  {
    //MahonyAHRSupdateIMU( gxrs,  gyrs,  gzrs , axg,  ayg,  azg);
    MahonyAHRSupdateIMU(gyrs, gzrs, gxrs, ayg, azg, axg);
    getRollPitchYaw_mahony();

   EulerAngle pitch, yaw, roll;

    initializeEulerAngle(&pitch);
    initializeEulerAngle(&yaw);
    initializeEulerAngle(&roll);

    pitch.value = pitch_mahony;
    yaw.value = yaw_mahony;
    roll.value = roll_mahony;

    float pitchCorrigido = 0;
    float yawCorrigido = 0;
    float rollCorrigido = 0;

     pitchCorrigido = corrigeAngulo(&pitch);
     yawCorrigido = corrigeAngulo(&yaw);
     rollCorrigido = corrigeAngulo(&roll);

    Serial.print(yawCorrigido);
    Serial.print(" ");
    Serial.print(pitchCorrigido);
    Serial.print(" ");
    Serial.print(rollCorrigido);
    Serial.print(" ");
    Serial.println();


     SerialBT.print(yawCorrigido);
    SerialBT.print(" ");
    SerialBT.print(pitchCorrigido);
    SerialBT.print(" ");
    SerialBT.print(rollCorrigido);
    SerialBT.print(" \n");
    

    //gesto = maquinaGestos_v2(derivaYaw(yaw_mahony), derivaPitch(pitch_mahony), g_clique);
    // atividade = interpretaGestos(gesto);
    // scroll = scrollDetector();
    // if(atividade == false)
    // {
    //   xchg = 0;
    //   ychg = 0;
    //   scroll = 0;
    // }
    //dwellClick(xchg, ychg, scroll);
   
  }
  // counter ++;


}

