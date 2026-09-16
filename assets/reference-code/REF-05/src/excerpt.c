/* C (C89): declarations first, then statements */
void shuffle(int *deck, int count)
{
    int i;
    int j;
    int temp;
    for (i = count - 1; i > 0; i--) {
        j = rand() % (i + 1);
        temp = deck[i]; deck[i] = deck[j]; deck[j] = temp;
    }
    /* int late = 0;   <- not allowed in C89 after a statement */
}
