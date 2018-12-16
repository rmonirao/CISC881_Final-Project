clear all
close all
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
P1 = imread('patch1.png');
P2 = imread('patch2.png');
P3 = imread('patch3.png');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%Patch 1

hold off
S_P1=P1(:,:,2);         % taking a slice of the image in the middle
figure (1);
title ('Patch1');
imshow(S_P1);

hold off                % Sliced Histrogram 
figure (4);
imhist (S_P1);
title ('Histrogram Patch1');
ylabel ('Frequency');
xlabel ('Pixel Intensity');

hold off                % Equalization Plot
figure (5);
K=histeq (S_P1);
title ('Equalization Plot Patch1');
imshow(K);

hold off                % Histrogram of Equalization
figure (6);
imhist (K);
title ('Histrogram Equalized Patch1');
ylabel ('Frequency');
xlabel ('Pixel Intensity');

hold off
figure (13);
subplot (2,1,1);
imshow (S_P1)
title ('Patch 1');

subplot (2,1,2);
imshow (K);
title ('Equalization Plot Patch1');

hold off
figure (14);
subplot (2,1,1);
imhist (S_P1);
title ('Histrogram Patch1');
ylabel ('Frequency');
xlabel ('Pixel Intensity');

subplot (2,1,2);
imhist (K);
title ('Histrogram Equalized Patch1');
ylabel ('Frequency');
xlabel ('Pixel Intensity');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Patch 2

hold off
S_P2=P2(:,:,2);         % taking a slice of the image in the middle
figure (2);
title ('Patch2');
imshow(S_P2);

hold off                % Sliced Histrogram 
figure (7);
imhist (S_P2);
title ('Histrogram Patch2');
ylabel ('Frequency');
xlabel ('Pixel Intensity');

hold off                % Equalization Plot
figure (8);
K2=histeq (S_P2);
title ('Equalization Plot Patch2');
imshow(K2);

hold off                % Histrogram of Equalization
figure (9);
imhist (K2);
title ('Histrogram Equalized Patch2');
ylabel ('Frequency');
xlabel ('Pixel Intensity');

hold off
figure (15);
subplot (2,1,1);
imshow (S_P2)
title ('Patch 2');

subplot (2,1,2);
imshow (K2);
title ('Equalization Plot Patch2');

hold off
figure (16);
subplot (2,1,1);
imhist (S_P2);
title ('Histrogram Patch2');
ylabel ('Frequency');
xlabel ('Pixel Intensity');

subplot (2,1,2);
imhist (K2);
title ('Histrogram Equalized Patch2');
ylabel ('Frequency');
xlabel ('Pixel Intensity');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Patch 3

hold off
S_P3=P3(:,:,2);         % taking a slice of the image in the middle
figure (3);
title ('Patch3');
imshow(S_P3);

hold off                % Sliced Histrogram 
figure (10);
imhist (S_P3);
title ('Histrogram Patch3');
ylabel ('Frequency');
xlabel ('Pixel Intensity');

hold off                % Equalization Plot
figure (11);
K3=histeq (S_P3);
title ('Equalization Plot Patch3');
imshow(K3);

hold off                % Histrogram of Equalization
figure (12);
imhist (K3);
title ('Histrogram Equalized Patch3');
ylabel ('Frequency');
xlabel ('Pixel Intensity');

hold off
figure (17);
subplot (2,1,1);
imshow (S_P3)
title ('Patch 3');

subplot (2,1,2);
imshow (K3);
title ('Equalization Plot Patch3');

hold off
figure (18);
subplot (2,1,1);
imhist (S_P3);
title ('Histrogram Patch3');
ylabel ('Frequency');
xlabel ('Pixel Intensity');

subplot (2,1,2);
imhist (K3);
title ('Histrogram Equalized Patch3');
ylabel ('Frequency');
xlabel ('Pixel Intensity');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%