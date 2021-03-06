"""Script for making html from a directory.
"""
# Sample usage:
# (box3d_shape_ft) python make_html.py --imgs_root_dir='/data0/shubhtuls/code/oc3d/cachedir/results_vis/box3d/val/box3d_shape_ft' --html_name=box3d_shape_ft --html_dir='/data0/shubhtuls/code/oc3d/cachedir/results_vis/pages/'

# (dwr_shape_ft) python make_html.py --imgs_root_dir='/data0/shubhtuls/code/oc3d/cachedir/results_vis/dwr/val/dwr_shape_ft' --html_name=dwr_shape_ft --html_dir='/data0/shubhtuls/code/oc3d/cachedir/results_vis/pages/'

# (depth_baseline) python make_html.py --imgs_root_dir='/data0/shubhtuls/code/oc3d/cachedir/results_vis/depth_baseline' --html_name=depth_baseline --html_dir='/data0/shubhtuls/code/oc3d/cachedir/results_vis/pages/'

# (voxels_baseline) python make_html.py --imgs_root_dir='/data0/shubhtuls/code/oc3d/cachedir/results_vis/voxels_baseline' --html_name=voxels_baseline --html_dir='/data0/shubhtuls/code/oc3d/cachedir/results_vis/pages/'

# (nyu) python make_html.py --imgs_root_dir='/data0/shubhtuls/code/oc3d/cachedir/results_vis/nyu/test/dwr_shape_ft' --html_name=nyu_dwr_shape_ft --html_dir='/data0/shubhtuls/code/oc3d/cachedir/results_vis/pages/'

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from absl import app
from absl import flags
import os
import os.path as osp
from yattag import Doc
from yattag import indent
import numpy as np
import json
import pdb
flags.DEFINE_string('imgs_root_dir', '', 'Directory where renderings are saved')
flags.DEFINE_string('html_name', None, 'Name of webpage')
flags.DEFINE_string('html_dir', '', 'Directory where output should be saved')
flags.DEFINE_boolean('hide_keys', True, 'Hide images with keys')
flags.DEFINE_string('filename_ordering', None, 'Ordering of files')
flags.DEFINE_string('vis_dirs', None, 'File names to visualize')

def draw_json_table(json_path, doc_tags):
    doc, tag, text = doc_tags
    with open(json_path) as f:
        bench_stats = json.load(f)

    bench_stats = bench_stats['bench']
    bench_stats.pop('total')
    bench_stats.pop('correct')
    bench_stats.pop('acc_rel_dir')
    bench_stats.pop('rel_dir')
    bench_stats.pop('acc_rel_quat')
    bench_stats.pop('pwd')
    bench_stats.pop('pwr')

    # pdb.set_trace()
    keys = bench_stats.keys()
    datas = []
    with tag('td'):
        with tag('table', border="1"):
            i = 0
            with tag('tr'):
                for key in keys:
                    with tag('td'):
                        text(key)
                    datas.append(bench_stats[key])
                    i += 1
                # pdb.set_trace()
            for d in zip(*datas):
                with tag('tr'):
                    for indv_d in d:
                        with tag('td'):
                            text("{0:.3f}".format(indv_d))


def main(_):

    opts = flags.FLAGS
    # pdb.set_trace()
    vis_dir_names = vis_dir_names_from_file = os.listdir(opts.imgs_root_dir)
    vis_dir_names.sort()
    if opts.filename_ordering is not None:
        vis_dir_names = json.load(open(opts.filename_ordering))

    if opts.vis_dirs is not None:
        vis_dir_names = []
        with open(opts.vis_dirs) as f:
            for line in f:
                vis_dir_names.append(line.strip())


    img_root_rel_path = osp.relpath(opts.imgs_root_dir, opts.html_dir)
    if not os.path.exists(opts.html_dir):
        os.makedirs(opts.html_dir)

    if opts.html_name is None:
        print('html_name is necessary')
        return

    html_file = osp.join(opts.html_dir, opts.html_name + '.html')
    ctr = 0
    img_keys = os.listdir(osp.join(opts.imgs_root_dir, vis_dir_names[0]))
    img_keys.sort()
    # pdb.set_trace()
    img_keys = ['img_roi.png', 'img_rel_dir_gt.png', 'img_rel_dir_pred.png', 'bench_iter_0.json', 'c_gt_objects_cam_view.png', 'b_pred_objects_cam_view.png']
    # img_keys = ['img_roi.png']
    doc, tag, text = Doc().tagtext()
    doc_tags = (doc, tag, text)
    with tag('html'):
        with tag('body'):
            with tag('table', style = 'width:100%', border="1"):
                with tag('tr'):
                    with tag('td'):
                        text("Filename")
                    for img_name in img_keys:
                        with tag('td'):
                            text("{}".format(img_name))
                for img_dir in vis_dir_names:
                    with tag('tr'):
                        with tag('td'):
                            text("{}".format(img_dir))
                        ## Images from A
                        for img_name in img_keys:
                            if img_dir not in vis_dir_names_from_file:
                                continue
                            if 'json' in img_name:
                                json_path = osp.join(opts.imgs_root_dir, img_dir, img_name)
                                draw_json_table(json_path, doc_tags)
                                continue
                            with tag('td'):
                                with tag('img', width="640px", src=osp.join(img_root_rel_path, img_dir, img_name)):
                                    ctr += 1


    r1 = doc.getvalue()
    r2 = indent(r1)

    with open(html_file, 'wt') as f:
        f.write(r2)
    

if __name__ == '__main__':
    app.run(main)
