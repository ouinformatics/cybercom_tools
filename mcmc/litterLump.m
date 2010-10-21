function y = litterLump(litterTime,litterValue)

L = length(litterTime);
d1=0;d2=0;d3=0;d4=0;d5=0;

for i = 1:L
    if(litterTime(i) <= 365)
        d1 = d1 + litterValue(i);
    end
    
    if((litterTime(i) > 365)&(litterTime(i) <= 2*365))
        d2 = d2 + litterValue(i);
    end
        
    if((litterTime(i) > 2*365)&(litterTime(i) <= 3*365))
        d3 = d3 + litterValue(i);
    end

    if((litterTime(i) > 3*365)&(litterTime(i) <= 4*365))
        d4 = d4 + litterValue(i);
    end

    if((litterTime(i) > 4*365)&(litterTime(i) <= 5*365))
        d5 = d5 + litterValue(i);
    end
end

y = [d1 d2 d3 d4 d5];