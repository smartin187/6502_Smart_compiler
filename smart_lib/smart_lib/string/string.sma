.string_count = 0;

.i_string = 0;

void count: ~str_count, .char_count {;
    .i_string = 0;
    .string_count = 0;
    while .i_string != 21 {;
        if ~str_count[.i_string] == .char_count {;
            .string_count++;
        }
        .i_string++;
    }
    return .string_count;
}

// void in: ~str_in, .char_in {;
//     .i_string = 0;
//     .string_count = 0; // 0 if not found, 1 if found

//     while .i_string != 21 {;
//         if ~str_in[.i_string] == .char_in {;
//             .string_count = 1;
//             break;
//         }
//         .i_string++;
//     }
//     return .string_count;
// }