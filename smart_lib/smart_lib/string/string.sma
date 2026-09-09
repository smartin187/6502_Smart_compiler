.string_count = 0;

.i = 0;

void count: ~str, .char {;
    .i = 0;
    .string_count = 0;
    while .i != 21 {;
        if ~str[.i] == .char {;
            .string_count++;
        }
        .i++;
    }
    return .string_count;
}