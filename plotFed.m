% MATLAB-skripti namukuvaajaa varten
close all
clear all

data = importdata('fedLog.txt',' ',0);
t=datetime(data(:,1),'ConvertFrom','posixtime');
dateNums = datenum(t);
lm = fitlm(dateNums,data(:,2),'linear');
tspace = linspace(min(dateNums)-0.3,max(dateNums)+1,size(dateNums,1))';
[ypred,yci] = predict(lm,tspace,'Alpha',0.01);

figure
hold on
trendi = plot(dateNums,data(:,2),'x--','Color',[86.3, 0, 42.4]./100,'LineWidth',1.6);
sovite = plot(tspace,ypred,'-','Color',[16.1, 3.9, 75.3]./100,'LineWidth',1.5);
confbounds = plot(tspace,yci,'--','Color',[100, 62.4, 0]./100,'LineWidth',1.3);
datetick('x','dd.mm.')

xlabel('Aika')
ylabel('Sy{\"o}tetyt namut')
title('Kisulin namujen m{\"a}{\"a}r{\"a} ajan funktiona')
legend('Trendik{\"a}yr{\"a}','Lineaarinen sovite','$99\%$-luottamusv{\"a}lit','location','SouthEast')
grid on
axis([dateNums(1)-0.3 dateNums(end)+1 min(data(:,2)) max(data(:,2))+20])
%hgsave(h, 'plotti.png');
print('plotti','-dpng')
