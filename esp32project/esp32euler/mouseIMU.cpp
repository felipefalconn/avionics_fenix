#include "mouseIMU.h"
#include <EEPROM.h>
int addr_eep = 0;
typedef struct 
{
  int x;
  int y;
  int z;

} calibration_t;

typedef union 
{
  calibration_t xyz;
  uint8_t buffer[12];
}calibrationUnion_t;

calibrationUnion_t calibValues;

extern float yaw_mahony, pitch_mahony, roll_mahony;

int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;
float axR, ayR, azR, gxR, gyR, gzR;
float axg, ayg, azg, gxrs, gyrs, gzrs;
float GyX_offset, GyY_offset, GyZ_offset;

int g_clique = 0;




void filtraIMU() {
  //Filtro 2 ordem
  // ax_filtro= filtro_2PB10Hz(AcX, pbax);
  // ay_filtro= filtro_2PB10Hz(AcY, pbay);
  // az_filtro= filtro_2PB10Hz(AcZ, pbaz);
  // gx_filtro= filtro_2PB10Hz(GyX, pbgx);
  // gy_filtro= filtro_2PB10Hz(GyY, pbgy);
  // gz_filtro= filtro_2PB10Hz(GyZ, pbgz);

  //Converte
  axg = (float)(AcX /*- LSM6DSM_AXOFFSET*/) / MPU6050_ACC_GAIN;
  ayg = (float)(AcY /*- LSM6DSM_AYOFFSET*/) / MPU6050_ACC_GAIN;
  azg = (float)(AcZ /*- LSM6DSM_AZOFFSET*/) / MPU6050_ACC_GAIN;
  gxrs = (float)(GyX - (calibValues.xyz.x)) / MPU6050_GYRO_GAIN * 0.01745329;  //degree to radians
  gyrs = (float)(GyY - (calibValues.xyz.y)) / MPU6050_GYRO_GAIN * 0.01745329;  //degree to radians
  gzrs = (float)(GyZ - (calibValues.xyz.z)) / MPU6050_GYRO_GAIN * 0.01745329;  //degree to radians
  // Degree to Radians Pi / 180 = 0.01745329 0.01745329251994329576923690768489
}
enum
{
  state_gx = 0,
  state_gy,
  state_gz,
};
#define SAMPLES 100
bool IMU_calibration()
{
    static bool calibrated = false;
    static int state = 0;
    static int counter = 0;
    static int samples_x = 0;
    static int samples_y = 0;
    static int samples_z = 0;
    byte value;
    
    //Read eeprom to look if the calibration has happened once
    value = EEPROM.read(addr_eep);
    
    if( value == 1)
    {
      calibrated = true;
      //copy the previous calibration offsets  
      int i = 0;
      for(i = 0;i<12;i++)
      {
        calibValues.buffer[i] = EEPROM.read(addr_eep+i+1);
      }
      Serial.print(value);
      Serial.print(" ");
      Serial.println();
      //TODO
    }
    else if(calibrated== false )
    {           
        digitalWrite(16, HIGH);
        if(counter < SAMPLES)
        {
          samples_x+=GyX;
          samples_y+=GyY;
          samples_z+=GyZ;
        }
        else
        {
            GyX_offset = samples_x/SAMPLES;
            GyY_offset = samples_y/SAMPLES;
            GyZ_offset = samples_z/SAMPLES;
            calibValues.xyz.x = GyX_offset;
            calibValues.xyz.y = GyY_offset;
            calibValues.xyz.z = GyZ_offset;

            EEPROM.write(addr_eep, 1);
            int i = 0;
            for(i = 0;i<12;i++)
            {
              EEPROM.write(addr_eep+i+1, calibValues.buffer[i]);
            }
            calibrated = true;
        }
        counter ++;
    }
    else
    {
      digitalWrite(16, LOW);
    }
    
    return calibrated;
}


float corrigeYaw(float sinal) {
  static float valorDeriv = 0, zero = 0;
  static float sinalCorrigido = 0, offset = 0;
  static float sinalAnterior = 0;
  static int s = 1, d = -1;

  valorDeriv = (sinal - zero);
  zero = sinal;

  if (valorDeriv <= -180) {
    offset += +360.0f;
  } else if (valorDeriv >= 180) {
    offset += -360.0f;
  }
  sinalCorrigido = sinal;
  sinalCorrigido += offset;

  return sinalCorrigido;
}
int mouseHoriz(void) {
  static float horzZero = 0.0f;
  static float horzValue = 0.0f;  // Stores current analog output of each axis
  static float yaw_corrigido = 0.0f;
  static int amostragem = 5;
  yaw_corrigido = corrigePitch(yaw_mahony);

  if (--amostragem == 0) {
    amostragem = 5;
    horzValue = (yaw_corrigido - horzZero) * SENSIBILIDADE;
    horzZero = yaw_corrigido;
  }
  return horzValue;
}
float corrigePitch(float sinal) {
  static float valorDeriv = 0, zero = 0;
  static float sinalCorrigido = 0, offset = 0;
  static float sinalAnterior = 0;
  static int s = 1, d = -1;

  valorDeriv = (sinal - zero);
  zero = sinal;

  if (valorDeriv <= -180) {
    offset += +360.0f;
  } else if (valorDeriv >= 180) {
    offset += -360.0f;
  }
  sinalCorrigido = sinal;
  sinalCorrigido += offset;

  return sinalCorrigido;
}




int mouseVert(void) {
  static float vertZero = 0.0f;
  static float vertValue = 0.0f;  // Stores current analog output of each axis
  static float pitch_corrigido = 0.0f;
  static int amostragem = 5;
  pitch_corrigido = corrigePitch(pitch_mahony);
  if (--amostragem == 0) {
    amostragem = 5;
    vertValue = (pitch_corrigido - vertZero) * SENSIBILIDADE;
    vertZero = pitch_corrigido;
  }
  return vertValue;
}




float derivaYaw(float sinal) {
  static float valorDeriv = 0;
  static float sinalCorrigido = 0, zero = 0;
  //static float zero = 0;
  sinalCorrigido = corrigeYaw(sinal);
  valorDeriv = (-1) * (sinalCorrigido - zero);
  zero = sinalCorrigido;
  return valorDeriv;
}
float derivaPitch(float sinal) {
  static float valorDeriv = 0;
  static float sinalCorrigido = 0, zero = 0;
  //static float zero = 0;
  sinalCorrigido = corrigePitch(sinal);
  valorDeriv = (sinalCorrigido - zero);
  zero = sinalCorrigido;
  return valorDeriv;
}

