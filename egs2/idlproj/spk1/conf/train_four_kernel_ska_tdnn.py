# SKA-TDNN with three kernel sizes 3,5,7 to attend to

# Frontend
frontend: melspec_torch
frontend_conf:
    preemp: true
    n_fft: 512
    log: true
    win_length: 400
    hop_length: 160
    n_mels: 80
    normalize: mn

# Encoder
encoder: four_kernel_ska_tdnn
encoder_conf:
  model_scale: 8
  ndim: 512
  ska_dim: 128
  output_size: 1536

# Pooling
pooling: chn_attn_stat

# Projector
projector: ska_tdnn
projector_conf:
  output_size: 192

# Preprocessor
preprocessor: spk
preprocessor_conf:
  target_duration: 3.0  # seconds
  sample_rate: 16000
  num_eval: 5
  noise_apply_prob: 0.5
  noise_info:
  - [1.0, 'dump/raw/musan_speech.scp', [4, 7], [13, 20]]
  - [1.0, 'dump/raw/musan_noise.scp', [1, 1], [0, 15]]
  - [1.0, 'dump/raw/musan_music.scp', [1, 1], [5, 15]]
  rir_apply_prob: 0.5
  rir_scp: dump/raw/rirs.scp

# Model conf
model_conf:
  extract_feats_in_collect_stats: false

# Loss
loss: aamsoftmax_sc_topk
loss_conf:
  margin: 0.3
  scale: 30
  K: 3
  mp: 0.06
  k_top: 5

# Training related
max_epoch: 40
num_att_plot: 0
num_workers: 4
cudnn_deterministic: False
cudnn_benchmark: True
drop_last_iter: True
iterator_type: category
valid_iterator_type: sequence
shuffle_within_batch: False
log_interval: 100
batch_size: 64
valid_batch_size: 32
use_amp: True
keep_nbest_models: 3
grad_clip: 9999
best_model_criterion:
- - valid
  - eer
  - min
num_iters_per_epoch: 2239

# Optimizer
optim: adam
optim_conf:
  lr: 0.001
  weight_decay: 0.00005
  amsgrad: False

# Scheduler
scheduler: CosineAnnealingWarmupRestarts
scheduler_conf:
  first_cycle_steps: 11195 # equal to 5 epochs
  cycle_mult: 1.0
  max_lr: 0.001    # 1e-3
  min_lr: 0.000005 # 5e-6
  warmup_steps: 1000
  gamma: 0.75