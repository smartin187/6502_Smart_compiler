._screen_conter = 0;
void screen_clean{;
    while True {;
        print: '\r';
        ._screen_conter = ._screen_conter + 1;

        if ._screen_conter == 24 {;
            break;
            }
        }
    }