writepm(512+1,7)
curATE = readpm(512+1)
printf("current ATE = %.0f\n", curATE)
printf("current sampling time = %.0f ns\n", 2^curATE*10)
printf("current sampling rate = %.0f S/s\n", 1/(2^curATE*1e-8))
printf("128 sampling time is %f s \n", 2^curATE*10e-9 * 128)
printf("256 sampling time is %f s \n", 2^curATE*10e-9 * 256)
printf("512 sampling time is %f s \n", 2^curATE*10e-9 * 512)

writepm(512+73,15)
curME = readpm(512+73)
printf("current ME = %.0f\n", curME)
printf("current memory size = %.0f \n", 2^curME)

%ndata = 512;
%[tS0 OK0] = readburstpm(0, 0, ndata-1, 512+24);
%printf("%f\n", tS0(1))
