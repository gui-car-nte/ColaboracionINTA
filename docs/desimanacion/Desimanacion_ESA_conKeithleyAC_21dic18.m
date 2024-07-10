
%%Fuente original:
% Desimanacion_ESA_DamasElche_feb2014
% Creado por:
% ANA BELEN FERNANDEZ DOMINGUEZ   (Feb del 2014)
% 
% Programa actual creado por:
% Jose Luis Mesa y Javier de Frutos (Nov de 2016)

%En este programa se lleva a cabo una desimanación en la que a cada paso la
%amplitud de la sinusoide va aumentando. Se combinan una fuente de precisión AC
%Keithley y una fuente de correinte alterna AC Agilent. La fuente Keithley
%mete hasta 100mA y la Agile0nt desde 100mA hasta el máximo.

clear all
close all
clc
% -------------------------------------------------------------------------
disp('A continuación aparecen los instrumentos abiertos con Matlab actualmente');

disp(instrfind);
disp(' ');
j=input('Si hay instrumentos abiertos, escribe "1" . Si no, escribe "0" ');
if j==0
    clc;
    end
if j==1
    instrfind;
    fclose(ans); delete(ans);clc;
end    
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------
% %
% FICHERO DONDE VOY A GUARDAR LOS DATOS DE CORRIENTE DE DC
% 
%disp('Por favor, guardar por proyectos. Ej.: C:\SENTINEL\Tipo-Medida_Fecha\...');
%ruta=input('Ruta para guardar el fichero con la última barra.', 's');
%nombre=input('nombre del archivo de subida   ', 's');
%nombre2=input('nombre del archivo de bajada   ', 's');

%ext='.dat';
%nombre_f=[ruta nombre ext];
%nombre_f2=[ruta nombre2 ext];

% Abro el archivo donde se van a ir guardando los datos
%fid=fopen(nombre_f ,'w');
%fprintf(fid,'    \t    \t    \t    \t    \t    \n');
%fprintf(fid,'Imedida(A)\t');
%fprintf(fid, 'Hora\t    Minuto\t    Segundo\t    Fechacompleta(s)\t    segundos_transcuirridos\t    Imedida(A)\n');

%fid2=fopen(nombre_f2 ,'w');
%fprintf(fid2,'    \t    \t    \t    \t    \t    \n');
%fprintf(fid,'Imedida(A)\t');
%fprintf(fid2, 'Hora\t    Minuto\t    Segundo\t    Fechacompleta(s)\t    segundos_transcuirridos\t    Imedida(A)\n');


%% EMPEZAMOS LLAMANDO A LOS EQUIPOS Y COLOCANDOLOS EN CERO

% % Se construye el string de dirección de la fuente:
strKei='GPIB0::13::INSTR';
interfaceKei = visa('agilent', strKei);
fopen(interfaceKei);
% Reseteammos la fuente y mandamos órdenes para comprobar posibles errores
fprintf(interfaceKei,'*RST');
fprintf(interfaceKei,'SOUR:WAVE:ABOR');
fprintf(interfaceKei,'SOUR:CLE');
fprintf(interfaceKei,'SOUR:WAVE:FUNC SIN');
fprintf(interfaceKei,'SOUR:WAVE:FREQ 3');
fprintf(interfaceKei,'SOUR:WAVE:DUR:TIME INF');

%Fuente AC
AC_source=visa('agilent','GPIB0::4::INSTR');
fopen(AC_source);
fprintf(AC_source,'*IDN?');
ID_AC = fscanf(AC_source);
disp(' ');
disp(ID_AC);
freq = 3;                                                                  % Hz
fprintf(AC_source,'FUNC SIN');
fprintf(AC_source,['SOUR:FREQ ',num2str(freq)]);
fprintf(AC_source,'OUTP:COUP DC');% Este comando es para imponer un modo de salida de Iout respecto de Vin que es = al que se usa en la calibración.
Vin=0;
fprintf(AC_source,['VOLT ',num2str(Vin)]);
fprintf(AC_source,'OUTP ON');
disp('Equipos reconocidos y conectados')
fprintf(AC_source,'OUTP OFF');

%% DETERMINAMOS EL CAMPO MAGNÉTICO MÁXIMO QUE VAMOS A METERLE 

pvs=input('¿qué porcentaje de variación quiere introducir en la rampa de subida? (PARA DESIMANACIÓN TIPO ESA PULSE 0)');
pvb=input('¿qué porcentaje de variación quiere introducir en la rampa de bajada? (PARA DESIMANACIÓN TIPO ESA PULSE 0)');

if pvs==0
    pvs=2;
end
if pvb==0
    pvb=1;
end

% disp('Introduce the maximum magnetic field (uT)')
H_max=input('¿qué campo magnético máximo deseas que alcance la desimanación?(PARA DESIMANACIÓN TIPO ESA (4000 uT) PULSE 0)');
if H_max==0
    H_max=4000;
end
H_max=(2*H_max);

%%%%%Para que salga bien en la fuente de AC (Esto es específico para 3 Hz y
%%%%%hay que calcularlo en caso de querer otra frecuencia)
H_max=(H_max+11.03896104)/1.81493506; %IMP específico de cada frec.esta es para 3Hz requisito ESA
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


disp (' ');
Cal = 611.981;   %Bobinas "Damas de Elche"                                  % (uT/A).
I_max = H_max / Cal;

disp('Press any key to start the magnetic ramp')
pause

%% COMENZAMOS LA RAMPA DE SUBIDA.

%La primera parte de la rampa se realiza con la fuente Keithley (Hasta los
%100 mA de corriente
%% _______________________________________________________________________
%  ________________________SUBIDA KEITHLEY________________________________
% Reseteammos la fuente
fprintf(AC_source,'OUTP OFF');
fprintf(interfaceKei,'*RST');
fprintf(interfaceKei,'SOUR:WAVE:ABOR');
fprintf(interfaceKei,'SOUR:CLE');
fprintf(interfaceKei,'SOUR:WAVE:FUNC SIN');
fprintf(interfaceKei,'SOUR:WAVE:FREQ 3');
fprintf(interfaceKei,'SOUR:WAVE:DUR:TIME INF');
% Introducimos el valor que define el rango.
fprintf(interfaceKei,'SOUR:WAVE:AMPL 0.1e-3');
fprintf(interfaceKei,'SOUR:WAVE:ARM');
Iampl=0.0001;
fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
pause(0.1);
% Iniciamos la fuente
fprintf(interfaceKei,'SOUR:WAVE:INIT');
Iampl=0.00004; %Que es lo necesario para generar 0.03uT
fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
j=1;
tic
     while Iampl<0.2e-3
        I=Iampl;
        Subida(j)=I;
        Istep_dosporciento=(Iampl*pvs)/100;
        Iampl=Iampl+Istep_dosporciento;
        fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
        ciclo=1/3;
        pause(ciclo)
        j=j+1;
     end
     
segundos1=toc;
strcat('Rango 1-Keithley-Tiempo de subida =',num2str(segundos1),'segundos')
%disp(segundos11);
fprintf(interfaceKei,'SOUR:WAVE:ABOR');

% % Subida fuente paso 2

fprintf(interfaceKei,'SOUR:WAVE:AMPL 10e-3');
fprintf(interfaceKei,'SOUR:WAVE:ARM');
Iampl=Iampl;
fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
fprintf(interfaceKei,'SOUR:WAVE:INIT');
fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
tic
     while Iampl<10e-3
        I=Iampl;
        Subida(j)=I;
        Istep_dosporciento=(Iampl*pvs)/100;
        Iampl=Iampl+Istep_dosporciento;
        fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
        ciclo=1/3;
        pause(ciclo)
        j=j+1;
     end
     
segundos2=toc;
strcat('Rango 2-Keithley-Tiempo de subida =',num2str(segundos2),'segundos')

fprintf(interfaceKei,'SOUR:WAVE:ABOR');

% % Subida fuente paso 3

fprintf(interfaceKei,'SOUR:WAVE:AMPL 105e-3');
fprintf(interfaceKei,'SOUR:WAVE:ARM');
Iampl=Iampl;
fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
fprintf(interfaceKei,'SOUR:WAVE:INIT');
fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
tic
     while Iampl<100e-3
        I=Iampl;
        Subida(j)=I;
        Istep_dosporciento=(Iampl*pvs)/100;
        Iampl=Iampl+Istep_dosporciento;
        fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
        ciclo=1/3;
        pause(ciclo)
        j=j+1;
     end
     
segundos3=toc;
strcat('Rango 3-Keithley-Tiempo de subida =',num2str(segundos3),'segundos')
%disp(segundos31);
fprintf(interfaceKei,'SOUR:WAVE:ABOR');
beep
% ---------------------------------------------------------------------------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% ________________________________________________________________________
%____________________________SUBIDA DE AC__________________________________
tic
fprintf(AC_source,'OUTP ON');
if Iampl>0.100
        i=1;
     while Iampl<I_max
        I=Iampl;
        Subida(j)=I;
        Vin = (Iampl-0.0078)/0.1747;
        P(i,:)=[Iampl Vin];
        fprintf(AC_source,['VOLT ',num2str(Vin)]);
        Istep_dosporciento=(Iampl*pvs)/100;
        Iampl=Iampl+Istep_dosporciento;
        ciclo=1/4; 
%         Se utilliza ciclo=1/4 para que la fuente Agilent responda a
%         tiempo al cambio de amplitud. Escucha más lento de lo que Matlab
%         envía.
        pause(ciclo)
        j=j+1;
        i=i+1;
     end
end
segundos4=toc;
beep
strcat('Rango 4-AC-Tiempo de subida =',num2str(segundos4),'segundos')

%% ________________________________________________________________________
%____________________________BAJADA DE AC__________________________________
%IAMPL SERÁ LA ÚLTIMA QUE TENGAMOS 
tic
if Iampl>0.100
      
        i=1;
     while Iampl>0.100
        I=Iampl;
        Subida(j)=I;
        Vin = (Iampl-0.0078)/0.1747;
        P(i,:)=[Iampl Vin];
        fprintf(AC_source,['VOLT ',num2str(Vin)]);
        Istep_unoporciento=(Iampl*pvb)/100;
        Iampl=Iampl-Istep_unoporciento;
        ciclo=1/4;
        pause(ciclo)
        j=j+1;
        i=i+1;
     end
end
 
 segundos5=toc;
strcat('Rango 5-AC-Tiempo de bajada =',num2str(segundos5),'segundos')
beep
  
    %% ________________________________________________________________________
%____________________________BAJADA DE KEITHLEY__________________________________

% Empieza la bajada con la Keithley
fprintf(AC_source,'OUTP OFF');
fprintf(interfaceKei,'SOUR:WAVE:AMPL 105e-3');
fprintf(interfaceKei,'SOUR:WAVE:ARM');
Iampl=Iampl;
fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
fprintf(interfaceKei,'SOUR:WAVE:INIT');
fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);

tic
     while Iampl>10e-3
        I=Iampl;
        Subida(j)=I;
        j=j+1;
        Istep_unoporciento=(Iampl*pvb)/100;
        Iampl=Iampl-Istep_unoporciento;
        fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
        ciclo=1/3;
        pause(ciclo)
     end
     
segundos6=toc;
strcat('Rango 6-Keithley-Tiempo de bajada =',num2str(segundos6),'segundos')
%disp(segundos32)
fprintf(interfaceKei,'SOUR:WAVE:ABOR');

% % Continua la bajada

fprintf(interfaceKei,'SOUR:WAVE:AMPL 10e-3');
fprintf(interfaceKei,'SOUR:WAVE:ARM');
Iampl=Iampl;
fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
pause(0.1);
fprintf(interfaceKei,'SOUR:WAVE:INIT');
fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
tic
     while Iampl>0.2e-3
        I=Iampl;
        Subida(j)=I;
        j=j+1;
        Istep_unoporciento=(Iampl*pvb)/100;
        Iampl=Iampl-Istep_unoporciento;
        fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
        ciclo=1/3;
        pause(ciclo)
     end
segundos7=toc;
strcat('Rango 6-Keithley-Tiempo de bajada =',num2str(segundos7),'segundos')
fprintf(interfaceKei,'SOUR:WAVE:ABOR');

% % Último paso de bajada

fprintf(interfaceKei,'SOUR:WAVE:AMPL 0.1e-3');
fprintf(interfaceKei,'SOUR:WAVE:ARM');
Iampl=Iampl;
fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
pause(0.1);
fprintf(interfaceKei,'SOUR:WAVE:INIT');
fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
tic
     while Iampl>4e-5
        I=Iampl;
        Subida(j)=I;
        j=j+1;
        Istep_unoporciento=(Iampl*pvb)/100;
        Iampl=Iampl-Istep_unoporciento;
        fprintf(interfaceKei,['SOUR:WAVE:AMPL ',num2str(Iampl)]);
        ciclo=1/3;
        pause(ciclo)
     end
 
segundos8=toc;
strcat('Rango 8-Keithley-Tiempo de bajada =',num2str(segundos8),'segundos')

fprintf(interfaceKei,'SOUR:WAVE:ABOR');

k=length(Subida);
x=[1:k];
semilogy(x,Subida)
grid on
xlabel('nº de ciclo')
ylabel('I(A)')

deltarangoK1=segundos1
deltarangoK2=segundos2
deltarangoK3=segundos3
deltarangoA4=segundos4
deltarangoA5=segundos5
deltarangoK6=segundos6
deltarangoK7=segundos7
deltarangoK8=segundos8