% Filename my_octave_script.m located in /Octave directory
pkg load instrument-control % to have tcpclient
pkg load io  % to have JSON

% send some random data
while(1);
    S = [];
    S0 = [];
    S1 = [];
    S2 = [];
    S3 = [];

    pause (0.001) % simulate the execution time your script needs
    % randdata = rand(1,100); % some random data to send
%    tic()

    ndata = 8;

    % DOP                               512 + 24, 512 + 31
    % standard normalization            S1, S2, S3 = 512 + 24, 512 + 25, 512 + 26
    % exact normalization               S1, S2, S3 = 512 + 32, 512 + 33, 512 + 34

    % normalizing value (default: 1000, 1uW) 512 + 38
    % non(or user-defined)-normalized   S1, S2, S3 = 512 + 39, 512 + 40, 512 + 41

    % raw data (32 bit) - integer part (16 bit) + fractional part (16 bit)
    % input POWER in uW          512 + 10, 512 + 11
    % S0          in uW          512 + 12, 512 + 13
    % S1          in uW          512 + 14, 512 + 15
    % S2          in uW          512 + 16, 512 + 17

    for i =0:15
        % [tDOP OK0] = readburstpm(0, ndata*i, ndata*(i+1)-1, 512+24);
        [tS1 OK1] = readburstpm(0, ndata*i, ndata*(i+1)-1, 512+25);
        [tS2 OK2] = readburstpm(0, ndata*i, ndata*(i+1)-1, 512+26);
        [tS3 OK3] = readburstpm(0, ndata*i, ndata*(i+1)-1, 512+27);

        %if OK0*OK1*OK2*OK3 == 1
        if OK1*OK2*OK3 == 1
            % tDOP = [tDOP tS0/2^15];
            S1 = [S1 (tS1-2^15)/2^15];
            S2 = [S2 (tS2-2^15)/2^15];
            S3 = [S3 (tS3-2^15)/2^15];
        end
    end
    S0 = 10*log10(readpm(512+10)/1000);
    DOP = readpm(512+24)/2^15;
    S= [S1 S2 S3 S0 DOP];

    tcpcli = tcpclient("127.0.0.1", 9999);
    write(tcpcli, toJSON(S));
%    toc()
end