import torch
from tqdm import tqdm


def load_prepare_nli(wrapper, data):
    max_len = 128

    labels_ar = []
    input_ids_ar = []
    attn_masks_ar = []
    segment_ids_ar = []

    for ex in tqdm(data):
        # 'ex' is a python dictionary
        premise = ex['premise'].numpy().decode('utf-8')
        hypothesis = ex['hypothesis'].numpy().decode('utf-8')

        encoded_dict = wrapper.tokenizer.encode_plus(premise, hypothesis,
                                                     max_length=max_len,
                                                     padding='max_length',
                                                     truncation=True,
                                                     return_tensors='pt')

        input_ids_ar.append(encoded_dict['input_ids'])
        attn_masks_ar.append(encoded_dict['attention_mask'])
        segment_ids_ar.append(encoded_dict['token_type_ids'])
        labels_ar.append(ex['label'].numpy())

    input_ids_ar = torch.cat(input_ids_ar, dim=0)
    attn_masks_ar = torch.cat(attn_masks_ar, dim=0)
    segment_ids_ar = torch.cat(segment_ids_ar, dim=0)

    labels_ar = torch.tensor(labels_ar)

    return input_ids_ar, attn_masks_ar, segment_ids_ar, labels_ar
