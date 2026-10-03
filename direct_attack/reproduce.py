"""Run independent checks with literal argv, captured stdout, hashes and provenance.

Default does not repeat the expensive enumeration. --full rebuilds search data.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent.parent

def seal_manifest():
    """Refresh and verify hashes after documentation/provenance-only edits."""
    target=ROOT/'direct_attack/data/sha256_manifest.json'
    manifest={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted((ROOT/'direct_attack').rglob('*')) if p.is_file()
              and '__pycache__' not in p.parts and p!=target
              and ('native_build' not in p.parts or p.name=='.gitignore')}
    target.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in manifest.items())
    return dict(files=len(manifest),verified=True)

def reproduction_commands():
    commands=[]
    for name in ['n3_binary','n4_binary','n5_binary_cover','n6_binary_cover',
                 'n3_ternary','n8_random','n10_ternary_random']:
        data=json.loads((ROOT/'direct_attack/data'/name/'summary.json').read_text())['arguments']
        argv=['-m','direct_attack.mine']
        for k in ['n','mode','alphabet','count','seed','out']: argv+=['--'+k,str(data[k])]
        commands.append(dict(source=name,argv=argv,
                             note='Reconstruction from saved arguments; original terminal stdout was not persisted.'))
    for n in [4,5,6]:
        argv=['-m','direct_attack.extremal','--n',str(n),'--out',f'direct_attack/data/n{n}_extremal']
        if n==4: argv+=['--minimum','9']
        commands.append(dict(source=f'n{n}_extremal',argv=argv))
    for name in ['n4_partition','n5_partition','n6_partition_random']:
        a=json.loads((ROOT/'direct_attack/data'/name/'summary.json').read_text())['arguments']
        argv=['-m','direct_attack.partition_attack']
        for k in ['n','mode','count','out']: argv+=['--'+k.replace('_','-'),str(a[k])]
        if a['stop_on_refutation']: argv+=['--stop-on-refutation']
        commands.append(dict(source=name,argv=argv))
    commands += [dict(source=name,argv=['-m','direct_attack.'+name]) for name in
                 ['pair_information','abstract_profile','bridge_obstruction','generalized_bridge','orientation_greedy','audit_unary','padding_obstruction']]
    for n in [4,5,6]:
        argv=['-m','direct_attack.history_dimensions','--n',str(n),'--out',f'direct_attack/data/n{n}_history_dimensions']
        if n>4: argv+=['--source',f'direct_attack/data/n{n}_extremal']
        commands.append(dict(source=f'n{n}_history_dimensions',argv=argv))
    commands.append(dict(source='bidirectional',argv=['-m','direct_attack.bidirectional','--source',
                    'direct_attack/data/n6_extremal','--random','2000','--n','7']))
    for root in sorted((ROOT/'direct_attack/data').glob('near_full_n*')):
        a=json.loads((root/'summary.json').read_text())['arguments']
        argv=['-m','direct_attack.near_full_search']
        for k in ['n','corank','iterations','seed','out']: argv+=['--'+k,str(a[k])]
        if a.get('minimum_protected') is not None: argv+=['--minimum-protected',str(a['minimum_protected'])]
        if a.get('source'):argv+=['--source',a['source']]
        if 'restart' in a:argv+=['--restart',str(a['restart'])]
        original_argv=list(argv)
        argv[argv.index('--out')+1]=str(root.relative_to(ROOT)).replace('\\','/')
        frozen=root/'input/seed.json'
        if a.get('source') and frozen.exists():
            argv[argv.index('--source')+1]=str(frozen.relative_to(ROOT)).replace('\\','/')
        record=dict(source=root.name,argv=argv)
        if argv!=original_argv:
            record.update(original_argv=original_argv,note='Raw summary arguments retained; archived output and frozen row seed override the relocated historical paths.')
        commands.append(record)
    commands.append(dict(source='cycle_insertion',argv=['-m','direct_attack.cycle_insertion']))
    commands.append(dict(source='image_extension_families',argv=['-m','direct_attack.image_extension_families']))
    commands.append(dict(source='top_rank_boundary',argv=['-m','direct_attack.top_rank_boundary']))
    for root in sorted((ROOT/'direct_attack/data').glob('image_extension_*')):
        path=root/'summary.json'
        if not path.exists():continue
        data=json.loads(path.read_text())
        if not isinstance(data,dict) or 'arguments' not in data:continue
        a=data['arguments']
        if 'rank_cover' in root.name:
            module='rank_cover';keys=['n','out']
        elif 'two_arms' in root.name:
            module='two_arm_mining';keys=['max_n','permutations','seed','out']
        elif 'broad' in root.name:
            module='image_policy_broad';keys=['n','alphabet','count','seed','restart','out']
            if 'objective' in a:keys.append('objective')
        elif 'policy_local_n' in root.name:
            module='local_policy_cover';keys=['n','alphabet','mode','count','seed','out']
        elif root.name=='image_extension_policy_n6' or 'policy_cover' in root.name:
            module='image_policy_cover';keys=['n','out']
            for k in ['alphabet','mode','count','seed']:
                if k in a:keys.append(k)
        elif 'policy_adversarial' in root.name:
            module='image_policy_adversarial';keys=['n','count','seed','out']
            if 'defect' in a:keys.append('defect')
        elif 'policy' in root.name:
            module='image_extension_policy';keys=['mode','count','seed','out']
            if a.get('n') is not None:keys=['n']+keys
        elif 'adversarial' in root.name:
            module='image_extension_adversarial';keys=['n','count','seed','out']
        else:
            module='image_extension';keys=['n','mode','count','seed','out']
            if a.get('source'):keys=['source']+keys
        argv=['-m','direct_attack.'+module]
        for k in keys:argv+=['--'+k.replace('_','-'),str(a[k])]
        commands.append(dict(source=root.name,argv=argv))
    commands += [dict(source=name,argv=['-m','direct_attack.'+name]) for name in
                 ['local_rank_family','fixed_arm_family','union_capacity_attack','policy_potentials','circular_image_policy','singleton_transport']]
    for module,maximum in [('alternating_extension',25),('alternating_frame',37)]:
        commands.append(dict(source=module,argv=['-m','direct_attack.'+module,'--max-n',str(maximum),
                        '--out','direct_attack/data/'+module+'_layer']))
    commands.append(dict(source='heredity_obstruction',argv=['-m','direct_attack.heredity_obstruction']))
    for path in sorted((ROOT/'direct_attack/data/alphabet_monotonicity').glob('*/summary.json')):
        a=json.loads(path.read_text())['arguments']
        argv=['-m','direct_attack.alphabet_monotonicity']
        for k in ['n','kind','out']:argv+=['--'+k,str(a[k])]
        commands.append(dict(source='alphabet_monotonicity/'+path.parent.name,argv=argv))
    commands.append(dict(source='anchored_image_bound',argv=['-m','direct_attack.anchored_image_bound']))
    commands.append(dict(source='shortcut_family',argv=['-m','direct_attack.shortcut_family','--max-n','22',
                    '--out','direct_attack/data/shortcut_family']))
    commands.append(dict(source='complete_union_obstruction',argv=['-m','direct_attack.complete_union_obstruction']))
    commands.append(dict(source='extremal_shortcuts',argv=['-m','direct_attack.extremal_shortcuts']))
    commands.append(dict(source='extremal_shortcut_pairs',argv=['-m','direct_attack.extremal_shortcuts','--pairs']))
    commands += [dict(source=name,argv=['-m','direct_attack.'+name]) for name in
                 ['three_image_family','one_fixed_family','transposition_extension_scan','adjacent_swap_family']]
    roots=sorted((ROOT/'direct_attack/data').glob('rank_three_extension_n*'))+sorted((ROOT/'direct_attack/data').glob('rank_bounded_extension_n*'))
    for root in roots:
        a=json.loads((root/'summary.json').read_text())['arguments']
        module='rank_bounded_extension_search' if 'rank' in a else 'rank_three_extension_search'
        argv=['-m','direct_attack.'+module]
        keys=['n','count','seed','restart']+(['rank','limit','seed_count'] if 'rank' in a else [])
        for key in keys:argv+=['--'+key.replace('_','-'),str(a[key])]
        for key in ['family_seed','elite','permutation_mutations']:
            if a.get(key):argv+=['--'+key.replace('_','-')]
        argv+=['--out',str(root.relative_to(ROOT)).replace('\\','/')]
        commands.append(dict(source=root.name,argv=argv,note='Initial stdout absent only for rank3 n12/20/30/40; full frozen replay outputs retained for all.'))
    commands += [dict(source=name,argv=['-m','direct_attack.'+name]) for name in
                 ['seed_budget_certificates','maximum_seed_family','seed_inclusion_attack']]
    for root in sorted((ROOT/'direct_attack/data').glob('seed_budget_*')):
        path=root/'summary.json'
        if not path.exists():continue
        a=json.loads(path.read_text()).get('arguments')
        if not a:continue
        argv=['-m','direct_attack.seed_budget_attack']
        for key in ['n','alphabet','count','seed','restart','mode','objective']:
            argv+=['--'+key,str(a[key])]
        if 'minimum_kappa' in a:argv+=['--minimum-kappa',str(a['minimum_kappa'])]
        argv+=['--out',str(root.relative_to(ROOT)).replace('\\','/')]
        commands.append(dict(source=root.name,argv=argv,note='Frozen input seeds and literal generation/replay child stdout and argv retained.'))
    commands.append(dict(source='short_reset_family',argv=['-m','direct_attack.short_reset_family']))
    commands.append(dict(source='irreducible_short_reset',argv=['-m','direct_attack.irreducible_short_reset']))
    commands.append(dict(source='circular_rank_area',argv=['-m','direct_attack.rank_area']))
    commands.append(dict(source='unit_tail_family',argv=['-m','direct_attack.unit_tail_family']))
    commands.append(dict(source='extremal_arbitrary_letters',argv=['-m','direct_attack.extremal_arbitrary_letters']))
    for root in sorted((ROOT/'direct_attack/data').glob('short_reset_policy_n*')):
        a=json.loads((root/'summary.json').read_text())['arguments'];argv=['-m','direct_attack.short_reset_policy_attack']
        for key in ['n','rank','alphabet','count','seed','restart']:argv+=['--'+key,str(a[key])]
        argv+=['--out',str(root.relative_to(ROOT)).replace('\\','/')]
        commands.append(dict(source=root.name,argv=argv,note='Frozen exact rows; mutation RNG advances through deterministic seed creation during replay. Literal generation and replay outputs retained.'))
    for module in ['permutation_units','unit_averaging','idempotent_boundary','commuting_unit_boundary','pu_prefix_certificates','gonze_image_bypass']:
        commands.append(dict(source=module,argv=['-m','direct_attack.'+module]))
    commands.append(dict(source='near_full_n18_r5/protected_peak',argv=['-c',
        'import json; from pathlib import Path; from direct_attack.near_full_search import score; '
        'r=Path("direct_attack/data/near_full_n18_r5"); z=json.loads((r/"best_010.json").read_text()); '
        'v,c=score(z["rows"],5,True); assert v==(12,12) and "reach_word" in c; '
        '(r/"protected_peak.json").write_text(json.dumps(c,indent=2)+chr(10),encoding="utf-8"); '
        'print(json.dumps(dict(value=v,reachable=True,compression_word=c["compression_word"],reach_word=c["reach_word"])))']))
    commands.append(dict(source='quotient_fiber_samples',
                         argv=['-m','direct_attack.quotient_fiber_samples']))
    commands.append(dict(source='congruence_extremal_scan',
                         argv=['-m','direct_attack.congruence_extremal_scan']))
    commands.append(dict(source='rank_two_period_cover',argv=[
        '-m','direct_attack.rank_two_period_audit','--max-n','8','--out',
        'direct_attack/data/rank_two_period_audit.json']))
    commands.append(dict(source='rank_two_two_cycle_family',argv=[
        '-m','direct_attack.rank_two_period_audit','--family-max-q','40','--out',
        'direct_attack/data/rank_two_two_cycle_family.json']))
    for p,q in [(4,5),(3,7),(4,6),(5,5),(4,7),(5,6),(5,7)]:
        commands.append(dict(source=f'rank_two_multi_perm_p{p}_q{q}',argv=[
            '-m','direct_attack.rank_two_multi_perm_search','--p',str(p),
            '--q',str(q),'--swap-i','0','--swap-j',str(p),'--out',
            f'direct_attack/data/rank_two_multi_perm_p{p}_q{q}.json']))
    commands.append(dict(source='one_fixed_all_permutations_n8',argv=[
        '-m','direct_attack.one_fixed_all_permutations','--n','8','--out',
        'direct_attack/data/one_fixed_all_permutations_n8.json']))
    for n in [4,5,6]:
        commands.append(dict(source=f'rank_two_two_perm_cover_n{n}',argv=[
            '-m','direct_attack.rank_two_two_perm_cover','--n',str(n),'--out',
            f'direct_attack/data/rank_two_two_perm_cover_n{n}.json']))
    commands.append(dict(source='rank_two_group_probe_n8',argv=[
        '-m','direct_attack.rank_two_group_probe','--n','8','--trials','100000',
        '--seed','20260930','--out','direct_attack/data/rank_two_group_probe_n8.json']))
    for n in [8,10]:
        commands.append(dict(source=f'rank_two_two_maps_probe_n{n}',argv=[
            '-m','direct_attack.rank_two_two_maps_probe','--n',str(n),
            '--trials','100000','--seed','20261001','--out',
            f'direct_attack/data/rank_two_two_maps_probe_n{n}.json']))
    for p,q in [(4,4),(4,5),(5,5),(5,6)]:
        commands.append(dict(source=f'rank_two_joint_nonsync_p{p}_q{q}',argv=[
            '-m','direct_attack.rank_two_joint_nonsync_cover','--p',str(p),
            '--q',str(q),'--out',
            f'direct_attack/data/rank_two_joint_nonsync_p{p}_q{q}.json']))
    for n in [4,5]:
        commands.append(dict(source=f'rank_three_color_cover_n{n}',argv=[
            '-m','direct_attack.rank_three_color_cover','--n',str(n),'--out',
            f'direct_attack/data/rank_three_color_cover_n{n}.json']))
    for n,trials,seed,flags,name in [
        (7,100000,20261002,[],'rank_three_color_boundary_n7'),
        (10,300000,20261003,[],'rank_three_color_boundary_n10'),
        (7,1000000,20261004,['--seek-stall'],'rank_three_color_stall_n7'),
        (7,1000000,20261005,['--seek-stall','--require-sc'],'rank_three_color_stall_sc_n7'),
        (4,300000,20261006,['--seek-stall','--require-sc'],'rank_three_color_stall_sc_n4'),
        (5,300000,20261006,['--seek-stall','--require-sc'],'rank_three_color_stall_sc_n5'),
        (6,300000,20261006,['--seek-stall','--require-sc'],'rank_three_color_stall_sc_n6')]:
        commands.append(dict(source=name,argv=[
            '-m','direct_attack.rank_three_color_boundary','--n',str(n),
            '--trials',str(trials),'--seed',str(seed),*flags,'--out',
            f'direct_attack/data/{name}.json']))
    for n,trials,seed,name in [
        (8,10000,20261007,'rank_three_two_perm_n8_10k'),
        (8,200000,20261008,'rank_three_two_perm_n8_200k'),
        (10,100000,20261009,'rank_three_two_perm_n10_100k')]:
        commands.append(dict(source=name,argv=[
            '-m','direct_attack.rank_three_two_perm_search','--n',str(n),
            '--trials',str(trials),'--seed',str(seed),'--out',
            f'direct_attack/data/{name}.json']))
    for n in [8,10,12]:
        commands.append(dict(source=f'rank_three_two_transposition_n{n}',argv=[
            '-m','direct_attack.rank_three_two_transposition_scan',
            '--n',str(n),'--out',
            f'direct_attack/data/rank_three_two_transposition_n{n}.json']))
    commands.append(dict(source='return_word_lift_search',argv=[
        '-m','direct_attack.return_word_lift','--trials','6000','--seed','20261011',
        '--out','direct_attack/data/return_word_lift_search.json']))
    commands.append(dict(source='mixed_rank_extension_n16',argv=[
        '-m','direct_attack.mixed_rank_extension_attack','--n','16','--count','50000',
        '--seed','20261012','--out','direct_attack/data/mixed_rank_extension_n16']))
    commands.append(dict(source='mixed_rank_extension_n24_fixed',argv=[
        '-m','direct_attack.mixed_rank_extension_attack','--n','24','--count','300000',
        '--rank-one','3','--rank-two','4','--seed','20261013',
        '--out','direct_attack/data/mixed_rank_extension_n24_fixed']))
    commands.append(dict(source='class_compression_pressure',argv=[
        '-m','direct_attack.class_compression_pressure','--trials','20000',
        '--seed','20261014','--out','direct_attack/data/class_compression_pressure.json']))
    commands.append(dict(source='bijective_fiber_returns',argv=[
        '-m','direct_attack.bijective_fiber_returns','--trials','3000',
        '--seed','20261015','--out','direct_attack/data/bijective_fiber_returns.json']))
    for trials,seed,limit,mode,name in [
        (120000,20261016,30000,'small','class_reset_pressure'),
        (1000000,20261017,150000,'large','class_reset_pressure_large')]:
        commands.append(dict(source=name,argv=['-m','direct_attack.class_reset_native',
            '--trials',str(trials),'--seed',str(seed),'--limit',str(limit),
            '--profile-mode',mode,'--out',f'direct_attack/data/{name}.json']))
    for trials,mode,name in [
        (1000000,'search','weighted_class_reset_pressure'),
        (2000,'search','weighted_class_reset_pressure_pilot'),
        (250000,'tiny','weighted_class_reset_tiny')]:
        commands.append(dict(source=name,argv=['-m','direct_attack.weighted_class_reset_native',
            '--trials',str(trials),'--seed','20261021','--mode',mode,
            '--out',f'direct_attack/data/{name}.json']))
    commands.append(dict(source='weighted_class_equality_lifts',argv=[
        '-m','direct_attack.weighted_class_equality_lifts']))
    commands.append(dict(source='compress_other_family',argv=[
        '-m','direct_attack.compress_other_family']))
    commands.append(dict(source='transposition_fold_obstruction',argv=[
        '-m','direct_attack.transposition_fold_obstruction']))
    commands.append(dict(source='two_cycle_image_obstruction',argv=[
        '-m','direct_attack.two_cycle_image_obstruction']))
    commands.append(dict(source='direct_binary_image_obstruction',argv=[
        '-m','direct_attack.direct_binary_image_obstruction']))
    commands.append(dict(source='log_dimension_history',argv=[
        '-m','direct_attack.log_dimension_history']))
    commands.append(dict(source='maximal_jump_log_history',argv=[
        '-m','direct_attack.maximal_jump_log_history']))
    commands.append(dict(source='optimal_log_history_n7',argv=[
        '-m','direct_attack.optimal_log_history_n7']))
    commands.append(dict(source='optimal_phase_independence',argv=[
        '-m','direct_attack.optimal_phase_independence']))
    commands.append(dict(source='shortest_binary_independence',argv=[
        '-m','direct_attack.shortest_binary_independence']))
    commands.append(dict(source='optimal_saturation_history',argv=[
        '-m','direct_attack.optimal_saturation_history']))
    commands.append(dict(source='optimal_counter_history',argv=[
        '-m','direct_attack.optimal_counter_history']))
    commands.append(dict(source='antipodal_corank_slack',argv=[
        '-m','direct_attack.antipodal_corank_slack']))
    commands.append(dict(source='avoid_compress_sharp_faces',argv=[
        '-m','direct_attack.avoid_compress_sharp_faces']))
    commands.append(dict(source='avoid_compress_third_face',argv=[
        '-m','direct_attack.avoid_compress_third_face']))
    commands.append(dict(source='avoid_compress_all_gaps',argv=[
        '-m','direct_attack.avoid_compress_all_gaps']))
    commands.append(dict(source='permutation_completion_boundary',argv=[
        '-m','direct_attack.permutation_completion_boundary']))
    commands.append(dict(source='original_kernel_graph_boundary',argv=[
        '-m','direct_attack.original_kernel_graph_boundary']))
    commands.append(dict(source='compress_other_lower_bound',argv=[
        '-m','direct_attack.compress_other_lower_bound']))
    commands.append(dict(source='corank_one_stability_quotient',argv=[
        '-m','direct_attack.corank_one_stability_quotient']))
    commands.append(dict(source='compress_other_short_reset',argv=[
        '-m','direct_attack.compress_other_short_reset']))
    commands.append(dict(source='annular_multicluster_boundary',argv=[
        '-m','direct_attack.annular_multicluster_boundary']))
    commands.append(dict(source='single_fiber_stability_boundary',argv=[
        '-m','direct_attack.single_fiber_stability_boundary']))
    commands.append(dict(source='full_history_boolean_capacity',argv=[
        '-m','direct_attack.full_history_boolean_capacity']))
    commands.append(dict(source='history_hyperplane_guards',argv=[
        '-m','direct_attack.history_hyperplane_guards']))
    commands.append(dict(source='balanced_history_rigidity',argv=[
        '-m','direct_attack.balanced_history_rigidity']))
    commands.append(dict(source='compress_other_non_sc_boundary',argv=[
        '-m','direct_attack.compress_other_non_sc_boundary']))
    commands.append(dict(source='singular_stationary_word_cost',argv=[
        '-m','direct_attack.singular_stationary_word_cost']))
    commands.append(dict(source='one_cluster_annular_controls',argv=[
        '-m','direct_attack.one_cluster_annular_controls']))
    commands.append(dict(source='paid_one_cluster_word',argv=[
        '-m','direct_attack.paid_one_cluster_word']))
    commands.append(dict(source='weak_stationary_linear_cost',argv=[
        '-m','direct_attack.weak_stationary_linear_cost']))
    commands.append(dict(source='almost_circular_returns',argv=[
        '-m','direct_attack.almost_circular_returns']))
    commands.append(dict(source='bounded_cerny_returns',argv=[
        '-m','direct_attack.bounded_cerny_returns']))
    commands.append(dict(source='fixed_root_cycle_extension',argv=[
        '-m','direct_attack.fixed_root_cycle_extension']))
    commands.append(dict(source='coprime_root_cycle_extension',argv=[
        '-m','direct_attack.coprime_root_cycle_extension']))
    commands.append(dict(source='kari_inverse_shrink',argv=[
        '-m','direct_attack.kari_inverse_shrink']))
    commands.append(dict(source='kari_shrink_products',argv=[
        '-m','direct_attack.kari_shrink_products']))
    commands.append(dict(source='original_defect_reversal',argv=[
        '-m','direct_attack.original_defect_reversal']))
    commands.append(dict(source='binary_balancing_boundary',argv=[
        '-m','direct_attack.binary_balancing_boundary']))
    commands.append(dict(source='moving_root_paid_compensation',argv=[
        '-m','direct_attack.moving_root_paid_compensation']))
    commands.append(dict(source='moving_root_amortized_return',argv=[
        '-m','direct_attack.moving_root_amortized_return']))
    commands.append(dict(source='moving_root_core_permutations',argv=[
        '-m','direct_attack.moving_root_core_permutations']))
    commands.append(dict(source='moving_root_coset_permutations',argv=[
        '-m','direct_attack.moving_root_coset_permutations']))
    commands.append(dict(source='moving_root_truncated_budget',argv=[
        '-m','direct_attack.moving_root_truncated_budget']))
    commands.append(dict(source='moving_root_order_two',argv=[
        '-m','direct_attack.moving_root_order_two']))
    commands.append(dict(source='reflection_core_tradeoff',argv=[
        '-m','direct_attack.reflection_core_tradeoff']))
    commands.append(dict(source='moving_root_all_high_order',argv=[
        '-m','direct_attack.moving_root_all_high_order']))
    commands.append(dict(source='short_root_return_square',argv=[
        '-m','direct_attack.short_root_return_square']))
    return commands

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--full',action='store_true'); args=ap.parse_args()
    data=ROOT/'direct_attack/data'; commands=reproduction_commands()
    (data/'reproduction_commands.json').write_text(json.dumps(commands,indent=2)+'\n',encoding='utf-8')
    checks=[['-m','direct_attack.check_profiles'],['-m','direct_attack.check_bridges'],
            ['-m','direct_attack.check_histories'],['-m','direct_attack.check_bidirectional'],
            ['-m','direct_attack.check_padding'],['-m','direct_attack.audit_unary'],
            ['-m','direct_attack.check_near_full'],['-m','direct_attack.check_cycle_insertion'],
            ['-m','direct_attack.check_vertex_covers'],
            ['-m','direct_attack.audit_cycle_mutations'],
            ['-m','direct_attack.check_image_extension'],['-m','direct_attack.check_image_policy'],
            ['-m','direct_attack.audit_image_mutations'],
            ['-m','direct_attack.top_rank_boundary'],
            ['-m','direct_attack.replay_image_search'],
            ['-m','direct_attack.check_native_policy'],
            ['-m','direct_attack.audit_native_small'],
            ['-m','direct_attack.check_new_image_results'],
            ['-m','direct_attack.audit_rank_cover'],
            ['-m','direct_attack.replay_policy_broad'],
            ['-m','direct_attack.circular_image_policy'],
            ['-m','direct_attack.policy_potentials'],
            ['-m','direct_attack.check_singleton_transport'],
            ['-m','direct_attack.check_alternating'],
            ['-m','direct_attack.check_heredity'],
            ['-m','direct_attack.check_alphabet_monotonicity'],
            ['-m','direct_attack.check_anchored_bound'],
            ['-m','direct_attack.audit_complete_policy'],
            ['-m','direct_attack.check_shortcut_family'],
            ['-m','direct_attack.check_complete_union'],
            ['-m','direct_attack.check_extremal_shortcuts'],
            ['-m','direct_attack.check_extremal_shortcuts','--pairs'],
            ['-m','direct_attack.check_union_defects'],
            ['-m','direct_attack.audit_sparse_policy'],
            ['-m','direct_attack.check_three_image_family'],
            ['-m','direct_attack.check_one_fixed_family'],
            ['-m','direct_attack.check_rank_three_search'],
            ['-m','direct_attack.replay_rank_three_search'],
            ['-m','direct_attack.check_adjacent_swap_family'],
            ['-m','direct_attack.check_transposition_extension_scan'],
            ['-m','direct_attack.check_first_drop'],
            ['-m','direct_attack.check_seed_budget','--out','reverse_independent_checks.json'],
            ['-m','direct_attack.audit_seed_binary_cover'],
            ['-m','direct_attack.replay_seed_budget_attack'],
            ['-m','direct_attack.check_maximum_seed_family'],
            ['-m','direct_attack.check_seed_inclusion'],
            ['-m','direct_attack.replay_seed_inclusion'],
            ['-m','direct_attack.check_short_reset'],
            ['-m','direct_attack.replay_short_reset'],
            ['-m','direct_attack.check_extremal_arbitrary'],
            ['-m','direct_attack.check_irreducible_short_reset'],
            ['-m','direct_attack.check_rank_area'],
            ['-m','direct_attack.check_unit_tail'],
            ['-m','direct_attack.check_permutation_units'],
            ['-m','direct_attack.check_unit_averaging'],
            ['-m','direct_attack.check_idempotent_boundary'],
            ['-m','direct_attack.check_commuting_unit_boundary'],
            ['-m','direct_attack.check_pu_prefix'],
            ['-m','direct_attack.check_gonze_bypass'],
            ['-m','direct_attack.check_quotient_fiber'],
            ['-m','direct_attack.check_congruence_extremal'],
            ['-m','direct_attack.check_quotient_lift_counter'],
            ['-m','direct_attack.check_rank_two_period','--out',
             'direct_attack/data/rank_two_period_independent_checks.json'],
            ['-m','direct_attack.check_rank_two_multi_perm','--out',
             'direct_attack/data/rank_two_multi_perm_independent_checks.json'],
            ['-m','direct_attack.check_one_fixed_all_permutations','--out',
             'direct_attack/data/one_fixed_all_permutations_n8_independent_checks.json'],
            ['-m','direct_attack.check_rank_two_permutation_alphabet','--out',
             'direct_attack/data/rank_two_permutation_alphabet_checks.json'],
            ['-m','direct_attack.check_rank_two_only_nonperm','--out',
             'direct_attack/data/rank_two_only_nonperm_checks.json'],
            ['-m','direct_attack.check_permutation_rainbow_first_drop','--out',
             'direct_attack/data/permutation_rainbow_first_drop_checks.json'],
            ['-m','direct_attack.check_rank_three_color_boundary','--out',
             'direct_attack/data/rank_three_color_boundary_n6_independent_checks.json'],
            ['-m','direct_attack.check_rank_three_color_boundary','--source',
             'direct_attack/data/rank_three_color_stall_sc_n7.json','--out',
             'direct_attack/data/rank_three_color_boundary_n7_independent_checks.json'],
            ['-m','direct_attack.check_rank_three_two_perm_search','--out',
             'direct_attack/data/rank_three_two_perm_independent_checks.json'],
            ['-m','direct_attack.check_rank_three_two_transposition_scan','--out',
             'direct_attack/data/rank_three_two_transposition_independent_checks.json'],
            ['-m','direct_attack.check_return_word_lift'],
            ['-m','direct_attack.check_class_compression_pressure'],
            ['-m','direct_attack.check_bijective_fiber_returns'],
            ['-m','direct_attack.check_terminal_kernel_frankl'],
            ['-m','direct_attack.check_class_reset_pressure'],
            ['-m','direct_attack.check_class_reset_pressure','--source',
             'direct_attack/data/class_reset_pressure.json','--out',
             'direct_attack/data/class_reset_pressure_small_checks.json'],
            ['-m','direct_attack.replay_fiber_continuation'],
            ['-m','direct_attack.audit_terminal_kernel_independent'],
            ['-m','direct_attack.check_return_monoid_independent_audit'],
            ['-m','direct_attack.check_terminal_window_barrier'],
            ['-m','direct_attack.capture_weighted_class_reset_checks'],
            ['-m','direct_attack.replay_weighted_class_reset'],
            ['-m','direct_attack.check_weighted_class_equality_lifts'],
            ['-m','direct_attack.replay_weighted_class_equality_lifts'],
            ['-m','direct_attack.check_permutation_averaging_word_cost_audit'],
            ['-m','direct_attack.check_compress_other_family'],
            ['-m','direct_attack.check_terminal_kernel_stagnation'],
            ['-m','direct_attack.check_short_rooted_word'],
            ['-m','direct_attack.check_transposition_fold_obstruction'],
            ['-m','direct_attack.check_fold_policy_chains'],
            ['-m','direct_attack.check_two_cycle_image_obstruction'],
            ['-m','direct_attack.check_direct_binary_image_obstruction'],
            ['-m','direct_attack.check_direct_binary_policy_chain'],
            ['-m','direct_attack.check_log_dimension_history'],
            ['-m','direct_attack.check_maximal_jump_log_history'],
            ['-m','direct_attack.check_optimal_log_history'],
            ['-m','direct_attack.check_optimal_phase_independence'],
            ['-m','direct_attack.check_shortest_binary_independence'],
            ['-m','direct_attack.check_optimal_saturation_history'],
            ['-m','direct_attack.check_optimal_counter_history'],
            ['-m','direct_attack.check_antipodal_corank_slack'],
            ['-m','direct_attack.check_avoid_compress_sharp_faces'],
            ['-m','direct_attack.check_avoid_compress_third_face'],
            ['-m','direct_attack.check_avoid_compress_all_gaps'],
            ['-m','direct_attack.check_permutation_completion_boundary'],
            ['-m','direct_attack.check_original_kernel_graph_boundary'],
            ['-m','direct_attack.check_compress_other_lower_bound'],
            ['-m','direct_attack.check_layered_pair_barrier_lean'],
            ['-m','direct_attack.check_corank_one_stability_quotient'],
            ['-m','direct_attack.check_compress_other_short_reset'],
            ['-m','direct_attack.check_annular_multicluster_boundary'],
            ['-m','direct_attack.check_single_fiber_stability_boundary'],
            ['-m','direct_attack.check_full_history_boolean_capacity'],
            ['-m','direct_attack.check_history_hyperplane_guards'],
            ['-m','direct_attack.check_nearcritical_n6_history'],
            ['-m','direct_attack.check_balanced_history_rigidity'],
            ['-m','direct_attack.check_binary_n6_history_cover'],
            ['-m','direct_attack.check_compress_other_non_sc_boundary'],
            ['-m','direct_attack.check_singular_stationary_word_cost'],
            ['-m','direct_attack.check_one_cluster_annular_controls'],
            ['-m','direct_attack.check_paid_one_cluster_word'],
            ['-m','direct_attack.check_weak_stationary_linear_cost'],
            ['-m','direct_attack.check_almost_circular_returns'],
            ['-m','direct_attack.check_bounded_cerny_returns'],
            ['-m','direct_attack.check_fixed_root_cycle_extension'],
            ['-m','direct_attack.check_coprime_root_cycle_extension'],
            ['-m','direct_attack.check_kari_inverse_shrink'],
            ['-m','direct_attack.check_kari_shrink_products'],
            ['-m','direct_attack.check_original_defect_reversal'],
            ['-m','direct_attack.check_binary_balancing_boundary'],
            ['-m','direct_attack.check_moving_root_paid_compensation'],
            ['-m','direct_attack.check_moving_root_amortized_return'],
            ['-m','direct_attack.check_moving_root_core_permutations'],
            ['-m','direct_attack.check_moving_root_coset_permutations'],
            ['-m','direct_attack.check_moving_root_truncated_budget'],
            ['-m','direct_attack.check_moving_root_order_two'],
            ['-m','direct_attack.check_reflection_core_tradeoff'],
            ['-m','direct_attack.check_moving_root_all_high_order'],
            ['-m','direct_attack.check_short_root_return_square'],
            ['-m','direct_attack.check_mixed_rank_extension','--root',
             'direct_attack/data/mixed_rank_extension_n16'],
            ['-m','direct_attack.check_mixed_rank_extension','--root',
             'direct_attack/data/mixed_rank_extension_n24_fixed'],
            ['-m','direct_attack.replay_return_and_mixed'],
            ['-c','import json; from pathlib import Path; from direct_attack.check_bridges import verify; '+
             'ps=sorted(Path("direct_attack/data/generalized_bridge").glob("C*.json")); '+
             'rs=[verify(json.loads(p.read_text())) for p in ps]; '+
             'print(json.dumps(dict(certificates=len(rs),vertices=sum(r["vertices"] for r in rs),verified=True)))'],
            ['-c','from direct_attack.abstract_profile import profile,audit; '+
             'rs=[audit(n,profile(n)) for n in [10,20,50,100,200,500,1000,2000]]; '+
             'print({"abstract_inequality_instances":len(rs),"verified":True})']]
    if args.full: checks=[r['argv'] for r in commands]+checks
    results=[]
    for argv in checks:
        start=datetime.now(timezone.utc).isoformat(); t=time.monotonic()
        r=subprocess.run([sys.executable]+argv,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        record=dict(argv=[sys.executable]+argv,cwd=str(ROOT),start_utc=start,
                    seconds=time.monotonic()-t,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr)
        results.append(record)
        print(json.dumps(dict(module=argv[1] if argv[0]=='-m' else 'inline audit',returncode=r.returncode,
                              seconds=record['seconds'])),flush=True)
        if r.returncode: break
    report=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),
                full_regeneration=args.full,runs=results,all_passed=all(r['returncode']==0 for r in results))
    (data/'audit_run.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    seal_manifest()
    if not report['all_passed']: raise SystemExit(1)

if __name__=='__main__': main()
