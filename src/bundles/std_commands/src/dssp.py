# vim: set expandtab ts=4 sw=4:

# === UCSF ChimeraX Copyright ===
# Copyright 2016 Regents of the University of California.
# All rights reserved.  This software provided pursuant to a
# license agreement containing restrictions on its disclosure,
# duplication and use.  For details see:
# http://www.rbvi.ucsf.edu/chimerax/docs/licensing.html
# This notice must be embedded in or attached to all copies,
# including partial copies, of the software or any revisions
# or derivations thereof.
# === UCSF ChimeraX Copyright ===

#
# Compute/assign secondary structure using Kabsch and Sander algorithm
#
def compute_ss(session, structures=None, *,
        min_helix_len=3, min_strand_len=3, energy_cutoff=-0.5, report=False):

    from chimerax.atomic import Structure
    from chimerax.dssp import compute_ss
    if structures is None:
        structures = [m for m in session.models.list() if isinstance(m, Structure)]
    elif isinstance(structures, Structure):
        structures = [structures]

    if len(structures) == 0:
        from chimerax.core.errors import UserError
        raise UserError('No structures specified')

    from chimerax.core.undo import UndoState
    undo_state = UndoState("dssp")
    for struct in structures:
        residues = struct.residues
        ss_types = residues.ss_types
        ss_ids = residues.ss_ids
        compute_ss(struct, energy_cutoff=energy_cutoff, min_helix_len=min_helix_len,
                   min_strand_len=min_strand_len, report=report)
        undo_state.add(residues, "ss_types", ss_types, residues.ss_types)
        undo_state.add(residues, "ss_ids", ss_ids, residues.ss_ids)

    session.undo.register(undo_state)

def register_command(logger):
    from chimerax.core.commands import CmdDesc, register, FloatArg, BoolArg, IntArg
    from chimerax.atomic import StructuresArg

    desc = CmdDesc(
        optional=[('structures', StructuresArg)],
        keyword=[('min_helix_len', IntArg),
                 ('min_strand_len', IntArg),
                 ('energy_cutoff', FloatArg),
                 ('report', BoolArg)],
        synopsis="compute/assign secondary structure using Kabsch & Sander DSSP algorithm"
    )
    register('dssp', desc, compute_ss, logger=logger)
