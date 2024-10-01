function control2(output_file)
    % set random seed --> otherwise always the same random number
    rng('shuffle')
    
    % get new random number of flashes between 1 and 10
    new_num_flash = randi(10,1);
    
    fileID = fopen(output_file, 'w');
    fprintf(fileID, '%d\n', new_num_flash);
    fclose(fileID);
end