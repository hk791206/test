import numpy as np

def compute_iou(box, boxes, box_area, boxes_area):
    """Calculates IoU of the given box with the array of the given boxes.
    box: 1D vector [y1, x1, y2, x2]
    boxes: [boxes_count, (y1, x1, y2, x2)]
    box_area: float. the area of 'box'
    boxes_area: array of length boxes_count.

    Note: the areas are passed in rather than calculated here for
    efficiency. Calculate once in the caller to avoid duplicate work.
    """
    # Calculate intersection areas
    y1 = np.maximum(box[0], boxes[:, 0])
    y2 = np.minimum(box[2], boxes[:, 2])
    x1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[3], boxes[:, 3])
    intersection = np.maximum(x2 - x1, 0) * np.maximum(y2 - y1, 0)
    union = box_area + boxes_area[:] - intersection[:]
    iou = intersection / union
    return iou

def compute_overlaps(boxes1, boxes2):
    """Computes IoU overlaps between two sets of boxes.
    boxes1, boxes2: [N, (y1, x1, y2, x2)].

    For better performance, pass the largest set first and the smaller second.
    """
    # Areas of anchors and GT boxes
    area1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    area2 = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])

    # Compute overlaps to generate matrix [boxes1 count, boxes2 count]
    # Each cell contains the IoU value.
    overlaps = np.zeros((boxes1.shape[0], boxes2.shape[0]))
    for i in range(overlaps.shape[1]):
        box2 = boxes2[i]
        overlaps[:, i] = compute_iou(box2, boxes1, area2[i], area1)
    return overlaps

def compute_recall(pred_boxes, gt_boxes, iou):
    """Compute the recall at the given IoU threshold. It's an indication
    of how many GT boxes were found by the given prediction boxes.

    pred_boxes: [N, (y1, x1, y2, x2)] in image coordinates
    gt_boxes: [N, (y1, x1, y2, x2)] in image coordinates
    """
    # Measure overlaps
    overlaps = compute_overlaps(pred_boxes, gt_boxes)
    iou_max = np.max(overlaps, axis=1)
    iou_argmax = np.argmax(overlaps, axis=1)
    positive_ids = np.where(iou_max >= iou)[0]
    matched_gt_boxes = iou_argmax[positive_ids]

    recall = len(set(matched_gt_boxes)) / gt_boxes.shape[0]
    return recall, positive_ids

def compute_matches(gt_boxes_classes,
                    pred_boxes_classes, pred_scores,
                    iou_threshold=0.5):
    """Finds matches between prediction and ground truth instances.

    Returns:
        gt_match: 1-D array. For each GT box it has the index of the matched
                  predicted box.
        pred_match: 1-D array. For each predicted box, it has the index of
                    the matched ground truth box.
        overlaps: [pred_boxes, gt_boxes] IoU overlaps.
    """
    print('gt_boxes_classes: ', gt_boxes_classes, '/', gt_boxes_classes.shape)
    print('pred_scores: ', pred_scores)

    # Loop through predictions and find matching ground truth boxes
    match_count = 0

    # Compute IoU overlaps [pred_masks, gt_masks]
    overlaps = compute_overlaps(pred_boxes_classes, gt_boxes_classes)

    pred_match = -1 * np.ones([pred_boxes_classes.shape[0]])
    gt_match = -1 * np.ones([gt_boxes_classes.shape[0]])
    for i in range(len(pred_boxes_classes)):
        # Find best matching ground truth box
        # 1. Sort matches by score
        sorted_ixs = np.argsort(overlaps[i])[::-1]
        # 2. Find the match
        for j in sorted_ixs:
            # If ground truth box is already matched, go to next one
            if gt_match[j] > -1:
                continue
            # If we reach IoU smaller than the threshold, end the loop
            iou = overlaps[i, j]
            if iou < iou_threshold:
                break
            # Do we have a match?
            if pred_boxes_classes[i, 4] == gt_boxes_classes[j, 4]:
                match_count += 1
                gt_match[j] = i
                pred_match[i] = j
                break

    print("gt_match: {}\n pred_match: {}\n match_count: {}".format(gt_match, pred_match, match_count))

    return gt_match, pred_match

annotation_path = 'dataset/annotation_val/annotation_val.txt'
with open(annotation_path) as f:
    lines = f.readlines()

n = len(lines)
print(n)
print(lines[0])

line = lines[0].split()
print(line)

box = np.array([np.array(list(map(int,box.split(',')))) for box in line[1:]])
print(box)

# test = [np.array(list(map(int,test.split(',')))) for test in line[1:]]
# print(type(test))
# print(test)

pred_box = np.array([np.array([822, 464, 841, 489, 0]), np.array([123, 123, 456, 456, 0]), np.array([915, 639, 946, 676, 0])])
print(pred_box.shape)
print(len(pred_box))
print(box[13, 0])
print(pred_box[:, 2])

a = compute_overlaps(pred_box, box)
print(a)
iou_max = np.max(a, axis=1)
print(iou_max)
iou_argmax = np.argmax(a, axis=1)
print(iou_argmax)

recall, positive_ids = compute_recall(pred_box, box, 0.5)
print(recall)
print(positive_ids)

gt_match, pred_match = compute_matches(box, pred_box, )

