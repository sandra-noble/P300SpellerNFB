 function experimental(output_file, accuracy_file)
    % get the accuracies from the last run
    accuracyFile = fileread(accuracy_file);
    accuracies = regexp(accuracyFile, 'Spelling accuracy:\s*\[([\d*.\d*\s*]*)\s*\]','tokens');
    last_acc = sscanf(accuracies{end}{1},'%f');
    prev_num_flash = length(last_acc);
    
    % calculate previous error in terms of J1
    prev_error = (100 - last_acc(end))/100;
    
    % calculate new number of flashes based on ILC update law
    delta = prev_num_flash/2;
    new_num_flash = ceil(prev_num_flash + delta * (2*prev_error-1));
    
    % flashes per row/col capped between 1 and 12
    if(new_num_flash < 1)
        new_num_flash = 1;
    elseif(new_num_flash > 12)
        new_num_flash = 12;
    end
   
    
    % write new number of flashes to file
    fileID = fopen(output_file, 'w');
    fprintf(fileID, '%d\n', new_num_flash);
    fclose(fileID);
end