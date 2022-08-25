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

    pause (0.005) % simulate the execution time your script needs
    % randdata = rand(1,100); % some random data to send
    ndata = 128;
    for i =1:100
        [tS0 OK0] = readburstpm(0, 0, ndata-1, 512+24);
        [tS1 OK1] = readburstpm(0, 0, ndata-1, 512+25);
        [tS2 OK2] = readburstpm(0, 0, ndata-1, 512+26);
        [tS3 OK3] = readburstpm(0, 0, ndata-1, 512+27);
        if OK0*OK1*OK2*OK3 == 1
            S0 = [S0 tS0];
            S1 = [S1 tS1];
            S2 = [S2 tS2];
            S3 = [S3 tS3];
        end
    end
    S= [S0 S1 S2 S3];

    % tic()
    tcpcli = tcpclient("127.0.0.1", 9999);
    write(tcpcli, toJSON(S));
    % toc()
end