from pyembroidery import EmbPattern, write_pes


def export_pes(filepath, stitch_sequences):

    pattern = EmbPattern()

    for seq in stitch_sequences:

        for stitch in seq.stitches:

            pattern.add_stitch_absolute(
                0,
                stitch.x,
                stitch.y
            )

    write_pes(pattern, filepath)