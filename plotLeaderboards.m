% MATLAB-skripti leaderboardseja varten
close all
clear all

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
%categorised = reordercats(categorised,users);categorised = categorical(users);


[bestAmounts, I] = maxk(amount,10);
bestCategorised = categorised(I);


figure
h = barh(removecats(bestCategorised), bestAmounts,'BarWidth',0.5,'FaceColor',[86.3, 0, 42.4]./100,'LineWidth',0.7);
set(gca,'TickLabelInterpreter','none')
ylabel('')
xlabel('Sy{\"o}t{\"o}t')
title('Top 10 Kisulin n{\"a}lk{\"a}sy{\"o}tt{\"a}j{\"a}t')
grid on

print('leaderboards','-dpng')
