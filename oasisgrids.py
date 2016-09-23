#!/usr/bin/env python

from __future__ import print_function

import sys, os
import argparse
import netCDF4 as nc
import numpy as np

from esm_grid import mom_grid, nemo_grid, t42_grid, fv300_grid

def check_args(args):

    err = None

    if args.model_name in ['MOM', 'NEMO']:
        if args.model_hgrid is None or \
            args.model_vgrid is None: \
            err = 'Please provide MOM or NEMO grid definition files.'

    return err

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("model_name", help="""
        The the model name. Supported names are:
            - MOM
            - NEMO
            - T42
            - FV300
            """)
    parser.add_argument("oasis_grid_name", help="""
        The OASIS name for the grid being created.
        """)
    parser.add_argument("--model_hgrid", default=None, help="""
        The model horizonatal grid definition file.
        Only needed for MOM and NEMO grids""")
    parser.add_argument("--model_vgrid", default=None, help="""
        The model vertical grid definition file.
        Only needed for MOM and NEMO grids""")
    parser.add_argument("--model_mask", default=None,help="""
        The model mask file.
        Only needed for MOM and NEMO grids""")
    parser.add_argument("--grids", default="grids.nc",
                        help="The path to output OASIS grids.nc file")
    parser.add_argument("--areas", default="areas.nc",
                        help="The path to output OASIS areas.nc file")
    parser.add_argument("--masks", default="masks.nc",
                        help="The path to output OASIS masks.nc file")

    args = parser.parse_args()

    err = check_args(args)
    if err is not None:
        print(err, file=sys.stderr)
        parser.print_help()
        return 1

    if args.model_name == 'MOM':
        model_grid = mom_grid.MomGrid(args.model_hgrid, args.model_vgrid,
                                      args.model_mask)
    elif args.model_name == 'NEMO':
        model_grid = nemo_grid.NemoGrid(args.model_hgrid, args.model_vgrid,
                                        args.model_mask)
    elif args.model_name == 'T42':
        model_grid = t42_grid.T42Grid()
    elif args.model_name == 'FV300':
        model_grid = fv300_grid.FV300Grid()
    else:
        assert False
    
    oasis_grid = OasisGrid(args.oasis_grid_name, model_grid)

    oasis_grid.write_grids(args.grids)
    oasis_grid.write_areas(args.areas)
    oasis_grid.write_masks(args.masks)


if __name__ == "__main__":
    sys.exit(main())
