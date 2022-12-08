##############################################################################
## Edited From https://github.com/lucidrains
##############################################################################

import torch
from torch import nn, einsum
from einops.layers.torch import Rearrange
from einops import rearrange, repeat, reduce
from einops_exts import rearrange_many, repeat_many, check_shape
import torch.nn.functional as F

from t5 import t5_encode_text, get_encoded_dim, DEFAULT_T5_NAME
from functools import partial

def exists(val):
    return val is not None

class PerceiverResampler(nn.Module):
    def __init__(
        self,
        *,
        dim,
        depth,
        dim_head = 64,
        heads = 8,
        num_latents = 64,
        num_latents_mean_pooled = 4, # number of latents derived from mean pooled representation of the sequence
        max_seq_len = 512,
        ff_mult = 4,
        cosine_sim_attn = False
    ):
        super().__init__()
        self.pos_emb = nn.Embedding(max_seq_len, dim)

        self.latents = nn.Parameter(torch.randn(num_latents, dim))

        self.to_latents_from_mean_pooled_seq = None

        if num_latents_mean_pooled > 0:
            self.to_latents_from_mean_pooled_seq = nn.Sequential(
                nn.LayerNorm(dim),
                nn.Linear(dim, dim * num_latents_mean_pooled),
                Rearrange('b (n d) -> b n d', n = num_latents_mean_pooled)
            )

        self.layers = nn.ModuleList([])
        for _ in range(depth):
            self.layers.append(nn.ModuleList([
                PerceiverAttention(dim = dim, dim_head = dim_head, heads = heads, cosine_sim_attn = cosine_sim_attn),
                FeedForward(dim = dim, mult = ff_mult)
            ]))

    def forward(self, x, mask = None):
        n, device = x.shape[1], x.device
        pos_emb = self.pos_emb(torch.arange(n, device = device))

        x_with_pos = x + pos_emb

        latents = repeat(self.latents, 'n d -> b n d', b = x.shape[0])

        if exists(self.to_latents_from_mean_pooled_seq):
            meanpooled_seq = masked_mean(x, dim = 1, mask = torch.ones(x.shape[:2], device = x.device, dtype = torch.bool))
            meanpooled_latents = self.to_latents_from_mean_pooled_seq(meanpooled_seq)
            latents = torch.cat((meanpooled_latents, latents), dim = -2)

        for attn, ff in self.layers:
            latents = attn(x_with_pos, latents, mask = mask) + latents
            latents = ff(latents) + latents

        return latents

class PerceiverAttention(nn.Module):
    def __init__(
        self,
        *,
        dim,
        dim_head = 64,
        heads = 8,
        cosine_sim_attn = False
    ):
        super().__init__()
        self.scale = dim_head ** -0.5 if not cosine_sim_attn else 1
        self.cosine_sim_attn = cosine_sim_attn
        self.cosine_sim_scale = 16 if cosine_sim_attn else 1

        self.heads = heads
        inner_dim = dim_head * heads

        self.norm = nn.LayerNorm(dim)
        self.norm_latents = nn.LayerNorm(dim)

        self.to_q = nn.Linear(dim, inner_dim, bias = False)
        self.to_kv = nn.Linear(dim, inner_dim * 2, bias = False)

        self.to_out = nn.Sequential(
            nn.Linear(inner_dim, dim, bias = False),
            nn.LayerNorm(dim)
        )

    def forward(self, x, latents, mask = None):
        x = self.norm(x)
        latents = self.norm_latents(latents)

        b, h = x.shape[0], self.heads

        q = self.to_q(latents)

        # the paper differs from Perceiver in which they also concat the key / values derived from the latents to be attended to
        kv_input = torch.cat((x, latents), dim = -2)
        k, v = self.to_kv(kv_input).chunk(2, dim = -1)

        q, k, v = rearrange_many((q, k, v), 'b n (h d) -> b h n d', h = h)

        q = q * self.scale

        # cosine sim attention

        if self.cosine_sim_attn:
            q, k = map(l2norm, (q, k))

        # similarities and masking

        sim = einsum('... i d, ... j d  -> ... i j', q, k) * self.cosine_sim_scale

        if exists(mask):
            max_neg_value = -torch.finfo(sim.dtype).max
            mask = F.pad(mask, (0, latents.shape[-2]), value = True)
            mask = rearrange(mask, 'b j -> b 1 1 j')
            sim = sim.masked_fill(~mask, max_neg_value)

        # attention

        attn = sim.softmax(dim = -1, dtype = torch.float32)
        attn = attn.to(sim.dtype)

        out = einsum('... i j, ... j d -> ... i d', attn, v)
        out = rearrange(out, 'b h n d -> b n (h d)', h = h)
        return self.to_out(out)

def FeedForward(dim, mult = 2):
    hidden_dim = int(dim * mult)
    return nn.Sequential(
        nn.LayerNorm(dim),
        nn.Linear(dim, hidden_dim, bias = False),
        nn.GELU(),
        nn.LayerNorm(hidden_dim),
        nn.Linear(hidden_dim, dim, bias = False)
    )

def masked_mean(t, *, dim, mask = None):
    if not exists(mask):
        return t.mean(dim = dim)

    denom = mask.sum(dim = dim, keepdim = True)
    mask = rearrange(mask, 'b n -> b n 1')
    masked_t = t.masked_fill(~mask, 0.)

    return masked_t.sum(dim = dim) / denom.clamp(min = 1e-5)

def l2norm(t):
    return F.normalize(t, dim = -1)


class TextEncoder(nn.Module):
    def __init__(self, cond_dim=512, output_dim=128,
                       attn_depth=2, attn_dim_head=64, attn_heads=8,
                       attn_num_latents=32, attn_cosine_sim_attn=False):
        super().__init__()
        self.text_encoder = partial(t5_encode_text, name=DEFAULT_T5_NAME)
        encoded_dim = get_encoded_dim(DEFAULT_T5_NAME)
        self.reduce_mapping = ReduceMapping(encoded_dim=encoded_dim, cond_dim=512, output_dim=128,
                       attn_depth=2, attn_dim_head=64, attn_heads=8,
                       attn_num_latents=32, attn_cosine_sim_attn=False)
    
    def forward(self, x:list, cpu=True):
        encoded_text = self.text_encoder(x, return_attn_mask=False)
        if cpu:
            encoded_text = encoded_text.cpu()
        cond_mean = self.reduce_mapping(encoded_text)
        return cond_mean


class ReduceMapping(nn.Module):
    def __init__(self, encoded_dim=512, cond_dim=512, output_dim=128,
                       attn_depth=2, attn_dim_head=64, attn_heads=8,
                       attn_num_latents=32, attn_cosine_sim_attn=False,
                       perceiver=True):
        super().__init__()
        self.encoded_dim = encoded_dim
        self.cond_dim = cond_dim
        self.output_dim = output_dim

        self.text_to_cond = nn.Linear(self.encoded_dim, cond_dim)
        self.attn_pool = PerceiverResampler(dim = cond_dim, depth = attn_depth, dim_head = attn_dim_head, heads = attn_heads, 
                                            num_latents = attn_num_latents, 
                                            cosine_sim_attn = attn_cosine_sim_attn) if perceiver else nn.Identity()
        self.to_text_non_attn_cond = nn.Sequential(
                        nn.LayerNorm(cond_dim, eps = 1e-5),
                        nn.Linear(cond_dim, self.output_dim),
                        nn.SiLU(),
                        nn.Linear(self.output_dim, self.output_dim)
                    )
    def forward(self, x:list):
        x = self.text_to_cond(x)
        x = self.attn_pool(x)
        x = x.mean(dim=-2)
        x = self.to_text_non_attn_cond(x)
        return x