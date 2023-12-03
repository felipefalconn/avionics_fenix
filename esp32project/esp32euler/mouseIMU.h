

#define SENSIBILIDADE 30
#define INVALIDO 0
#define SIM 1
#define NAO 2
#define MPU6050_ACC_GAIN 16384.0
#define MPU6050_GYRO_GAIN 131.072




void filtraIMU();
bool IMU_calibration();
float corrigeYaw(float sinal) ;
int mouseHoriz(void) ;
float corrigePitch(float sinal) ;
int mouseVert(void) ;
float derivaYaw(float sinal);
float derivaPitch(float sinal) ;
