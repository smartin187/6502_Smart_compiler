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

//.str_lenght = 0;

//void str_len: ~str_len {;
    // return the lenght of the string or list.
    // The length is the index+1 if last character not null.
    // Exemples:
    // str_len: "AAA" return 3
    // str_len: ['A', 'B', 'C', 0, 'A'] return 5 (the null byte at index 3 is counted)

//     .i_string = 0;
//     while .i_string != 21 {;
//         if ~str_len[20 -.i_string] != 0 {;
//             .str_lenght = 21 - .i_string;
//             break;
//         }
//         .i_string++;
//     }
//     return .str_lenght;
// }