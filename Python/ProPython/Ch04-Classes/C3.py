import itertools


def C3(cls, *mro_lists):
    # Make copies so you don't change existing content
    mro_lists = [list(mro_list[:]) for mro_list in mro_lists]

    # Setup new MRO with the class itself
    mro = [cls]

    while True:
        # Reset for next round of tests
        candidate_found = False

        for mro_list in mro_lists:
            if not len(mro_list):
                continue

            # Get first item as possible candidate for the MRO
            candidate = mro_list[0]

            if candidate_found:
                # Candidates promoted to the MRO are no longer of use
                if candidate in mro:
                    mro_list.pop(0)
                # Don't check for any more candidates if one was found.
                continue

            if candidate in itertools.chain(*(x[1:] for x in mro_lists)):
                # Candidate found in invalid position, move on to the
                # next MRO list to get a new candidate.
                continue
            else:
                # Candidate is valid and should get promoted to MRO
                mro.append(candidate)
                mro_list.pop(0)
                candidate_found = True
        if not sum(len(mro_list) for mro_list in mro_lists):
            # No more MROs to cycle through, return.
            break
        if not candidate_found:
            # No valid candidate was found. Bailing...
            raise TypeError('Inconsistent MRO')
    return mro
