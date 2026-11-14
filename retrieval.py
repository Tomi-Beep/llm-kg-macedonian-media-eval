def follow_link(facts, start, relation_name):
    matches = []

    for subject, relation, target in facts:
        if subject == start and relation == relation_name:
            matches.append(target)

    return matches


def find_graph_evidence(facts, film, needs_album):
    composers = follow_link(facts, film, "music_by")
    albums = []
    evidence = []

    for composer in composers:
        evidence.append(f'Музиката за филмот „{film}“ ја компонираше „{composer}“.')

        if needs_album:
            for album in follow_link(facts, composer, "released"):
                albums.append(album)
                evidence.append(f'„{composer}“ го издаде албумот „{album}“.')

    return composers, albums, evidence


def find_text_evidence(facts, film):
    catalogue = []

    for subject, relation, target in facts:
        if relation == "music_by":
            catalogue.append(f'Музиката за филмот „{subject}“ ја компонираше „{target}“.')
        elif relation == "released":
            catalogue.append(f'„{subject}“ го издаде албумот „{target}“.')

    text_matches = []

    for sentence in catalogue:
        if f'„{film}“' in sentence:
            text_matches.append(sentence)

    return text_matches