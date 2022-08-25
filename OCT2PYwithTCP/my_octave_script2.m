% Filename my_octave_script.m located in /Octave directory
pkg load instrument-control % to have tcpclient
pkg load io  % to have JSON

% send some random data
while(1);
    pause (0.020) % simulate the execution time your script needs
    randdata = rand(1,100); % some random data to send
    tcpcli = tcpclient("127.0.0.1", 9999);
    write(tcpcli, toJSON(randdata));
end
