void readkeys: *~line, .end {;
    .counter = 0;
    while .counter != 20 {;
        ~line[.counter] = input:;


        if ~line[.counter] == .end {;
            break;
        }


        .counter++;
    }
}
