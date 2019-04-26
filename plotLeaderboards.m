% MATLAB-skripti leaderboardseja varten
close all
clear all

% hassun hauskat tekstit
set(0,'defaultAxesFontName', 'Comic Sans MS')
set(0,'defaultTextFontName', 'Comic Sans MS')
set(groot, 'DefaultTextInterpreter', 'none')
set(groot, 'DefaultLegendInterpreter', 'none')
set(groot, 'defaultAxesTickLabelInterpreter','none')

data = string(importdata('leaderboardsLog.txt',' '));
datasplit = [];
timesplit = [];
for string = data'
    vector = strsplit(string);
    %timesplit = [timesplit; str2num(vector(1))];
    datasplit = [datasplit; vector];
end
namessplit = cellstr(datasplit(:,2));

users=unique(namessplit, 'stable');
amount=cell2mat(cellfun(@(x) sum(ismember(namessplit,x)),users,'un',0));
categorised = categorical(users);
categorised = reordercats(categorised,users);


[bestAmounts, I] = maxk3(amount,10);
bestCategorised = categorised(I);

tickStrings = cellstr(categorised);


figure
%removecats(bestCategorised),
h = barh( flip(bestAmounts),'BarWidth',0.5,'FaceColor',[86.3, 0, 42.4]./100,'LineWidth',0.7);
set(gca,'yticklabel', flip(tickStrings(I)) ); % R2016a bugfix
ylabel('')
xlabel('Namut')
title('Top 10 Kisulin Sugar Daddyt')
grid on

print('leaderboards','-dpng')
