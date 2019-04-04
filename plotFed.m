% MATLAB-skripti namukuvaajaa varten

close all
clear all

data = importdata('fedLog.txt',' ',0);
t=datetime(data(:,1),'ConvertFrom','posixtime');

figure
h = plot(t,data(:,2),'x--','Color',[86.3, 0, 42.4]./100,'LineWidth',2.2);
%stem(t,data(:,2))
xlabel('Aika')
ylabel('Sy{\"o}tetyt namut')
title('Kisulin namujen m{\"a}{\"a}r{\"a} ajan funktiona')
legend('Trendik{\"a}yr{\"a}','location','SouthEast')
grid on
%hgsave(h, 'plotti.png');
print('plotti','-dpng')