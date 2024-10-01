function control1(output_file, accuracy_file)
    % get the accuracies from the last run
    accuracyFile = fileread(accuracy_file);
    accuracies = regexp(accuracyFile, '[Ss]pelling accuracy:\s*\[([\d*.\d*\s*]*)\s*\]','tokens');
    last_acc = sscanf(accuracies{end}{1},'%f');
    prev_num_flash = length(last_acc);
    
    % determine next number of flashes
    % if more than 66% accuracy achieved, next number of flashes is average
    % between number used and minimum number needed to achieve 66%
    if(last_acc(end) > 66)
         for i=1:length(last_acc)
             if(last_acc(i) > 66)
                 min_flash = i;
                 break;
             end
         end
         
         new_num_flash = round((min_flash+prev_num_flash)/2);
         
    % if less than 66%, increase number of flashes by 1
    else
        new_num_flash = prev_num_flash + 1;
    end
    
    % write new number of flashes to file
    fileID = fopen(output_file, 'w');
    fprintf(fileID, '%d\n', new_num_flash);
    fclose(fileID);
end